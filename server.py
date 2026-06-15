"""
Servidor MCP — Conector Panel de Expertos (Chile)
v0.1 — endpoint del buscador verificado en vivo (06/2026)

El Panel de Expertos resuelve discrepancias del mercado eléctrico chileno.
Su buscador (http://64.202.184.231) consulta la biblioteca de documentos del
Panel (SharePoint, vía Microsoft Graph) y devuelve las discrepancias y sus
documentos.

API real (descubierta inspeccionando el sitio):
  GET  http://64.202.184.231/            -> entrega cookie de sesión + csrf-token
  POST http://64.202.184.231/search/documents        body {"query": "..."}
  POST http://64.202.184.231/search/documents/more    body {"link": "<nextLink>"}
  (descarga de archivo) /search/documents/download?id=<id>

Requiere la sesión de Laravel: primero GET para obtener cookie + token, luego
POST con el header X-CSRF-TOKEN.

Ejecución local (stdio):
    pip install -r requirements.txt
    python server.py
"""

import json
import logging
import re
import sys
import time
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("panel-expertos")

BUSCADOR = "http://64.202.184.231"
SEARCH = f"{BUSCADOR}/search/documents"
SEARCH_MORE = f"{BUSCADOR}/search/documents/more"
DOWNLOAD = f"{BUSCADOR}/search/documents/download"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
    "Accept-Language": "es-CL,es;q=0.9",
}

# --- Registro de uso (a stderr; no interfiere con stdio) ---------------------
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(message)s")
_logger = logging.getLogger("panel.uso")


def _log_uso(herramienta: str, **params) -> None:
    reg = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "tool": herramienta}
    reg.update({k: v for k, v in params.items() if v not in (None, "", False)})
    _logger.info(json.dumps(reg, ensure_ascii=False))


def _sesion_y_token() -> tuple[httpx.Client, Optional[str]]:
    """Abre una sesión, obtiene cookies de Laravel y el csrf-token del HTML."""
    c = httpx.Client(timeout=40, headers=HEADERS, follow_redirects=True)
    r = c.get(f"{BUSCADOR}/")
    m = re.search(r'name=["\']csrf-token["\']\s+content=["\']([^"\']+)["\']', r.text)
    return c, (m.group(1) if m else None)


def _anio_de(item: dict) -> Optional[str]:
    """Extrae el año desde el nombre (NN-YYYY) o desde la ruta/URL."""
    nombre = item.get("name", "") or ""
    m = re.match(r"\s*\d+\s*-\s*(\d{4})", nombre)
    if m:
        return m.group(1)
    url = item.get("webUrl", "") or ""
    m = re.search(r"/Discrepancias%20Tramitadas/(\d{4})/", url)
    return m.group(1) if m else None


def _numero_de(item: dict) -> Optional[str]:
    m = re.match(r"\s*(\d+\s*-\s*\d{4})", item.get("name", "") or "")
    return m.group(1).replace(" ", "") if m else None


@mcp.tool()
def buscar_discrepancias(
    consulta: str,
    anio: Optional[str] = None,            # filtrar por año, ej. "2025"
    solo_discrepancias: bool = True,       # True = solo carpetas (discrepancias); False = también documentos
    max_resultados: int = 50,
) -> dict:
    """Busca discrepancias del mercado eléctrico chileno resueltas por el Panel
    de Expertos. Búsqueda por texto libre sobre el nombre de cada discrepancia
    (que incluye número-año, partes involucradas y materia) y sus documentos.

    Devuelve número (ej. "24-2025"), nombre completo, año, tipo (discrepancia o
    documento), enlace en SharePoint y, para documentos, URL de descarga.

    Ejemplos:
      buscar_discrepancias("peaje de distribución")
      buscar_discrepancias("Engie contra CNE", anio="2024")
      buscar_discrepancias("acceso abierto transmisión", solo_discrepancias=False)
    """
    _log_uso("buscar_discrepancias", consulta=consulta, anio=anio,
             solo_discrepancias=solo_discrepancias)

    c, token = _sesion_y_token()
    cab = {
        "X-CSRF-TOKEN": token or "",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Referer": f"{BUSCADOR}/",
    }
    items: list[dict] = []
    try:
        r = c.post(SEARCH, headers=cab, json={"query": consulta})
        r.raise_for_status()
        data = r.json()
        body = data.get("body", {}) or {}
        items.extend(body.get("value", []) or [])
        next_link = body.get("@odata.nextLink")

        while next_link and len(items) < max_resultados * 3:
            r = c.post(SEARCH_MORE, headers=cab, json={"link": next_link})
            r.raise_for_status()
            d2 = r.json()
            b2 = d2.get("body", {}) or {}
            items.extend(b2.get("value", []) or [])
            next_link = d2.get("next_link") or b2.get("@odata.nextLink")
    finally:
        c.close()

    resultados = []
    vistos = set()
    for it in items:
        es_carpeta = "folder" in it
        es_archivo = "file" in it
        num = _numero_de(it)
        # En modo discrepancias: solo carpetas de primer nivel "NN-AAAA ..."
        # (descarta subcarpetas internas como "01.Actuaciones del Panel").
        if solo_discrepancias and not num:
            continue
        # evita duplicados por número
        if num and num in vistos:
            continue
        if num:
            vistos.add(num)
        anio_it = _anio_de(it)
        if anio and anio_it != str(anio):
            continue
        resultados.append({
            "numero": _numero_de(it),
            "nombre": it.get("name"),
            "anio": anio_it,
            "tipo": "discrepancia" if es_carpeta else ("documento" if es_archivo else "otro"),
            "url": it.get("webUrl"),
            "descarga": f"{DOWNLOAD}?id={it.get('id')}" if es_archivo else None,
            "creado": it.get("createdDateTime"),
            "modificado": it.get("lastModifiedDateTime"),
        })
        if len(resultados) >= max_resultados:
            break

    return {
        "consulta": consulta,
        "anio": anio,
        "total": len(resultados),
        "discrepancias": resultados,
        "fuente": "Panel de Expertos del mercado eléctrico de Chile (panelexpertos.cl)",
    }


if __name__ == "__main__":
    mcp.run()
