"""
Conector Panel de Expertos — versión REMOTA con OAuth (Streamable HTTP).

Reutiliza la herramienta de server.py (buscar_discrepancias) y la expone por
HTTP con OAuth 2.1 + registro dinámico de clientes (lo que Claude exige para
conectores remotos). Autorización de auto-aprobación (datos públicos).

URL pública: PUBLIC_URL o RAILWAY_PUBLIC_DOMAIN (fallback localhost).
"""

import base64
import os

from pydantic import AnyHttpUrl
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response

from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations

from assets import FAVICON_ICO_B64, FAVICON_PNG_B64
from auth_provider import ProveedorOAuthAutoAprobacion
from paginas import (
    FAVICON_SVG,
    LOGO_SVG,
    pagina_inicio,
    pagina_privacidad,
    pagina_terminos,
)
from server import buscar_discrepancias, leer_documento

CONTACTO = os.environ.get("CONTACTO_EMAIL", "contacto@bfly-cluster.ai")


def _url_publica() -> str:
    if os.environ.get("PUBLIC_URL"):
        return os.environ["PUBLIC_URL"].rstrip("/")
    dominio = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
    if dominio:
        return f"https://{dominio}"
    return f"http://localhost:{os.environ.get('PORT', '8000')}"


BASE = _url_publica()
_HOST = os.environ.get("RAILWAY_PUBLIC_DOMAIN") or BASE.split("://", 1)[-1]

auth = AuthSettings(
    issuer_url=AnyHttpUrl(BASE),
    resource_server_url=AnyHttpUrl(f"{BASE}/mcp"),
    client_registration_options=ClientRegistrationOptions(enabled=True),
    required_scopes=None,
)

mcp = FastMCP(
    "panel-expertos",
    auth_server_provider=ProveedorOAuthAutoAprobacion(),
    auth=auth,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8000")),
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[_HOST, f"{_HOST}:*", "localhost", "127.0.0.1"],
        allowed_origins=[f"https://{_HOST}", "https://claude.ai", "https://claude.com"],
    ),
)

mcp.tool(
    title="Buscar discrepancias del Panel de Expertos",
    annotations=ToolAnnotations(
        title="Buscar discrepancias del Panel de Expertos",
        readOnlyHint=True,
        destructiveHint=False,
        openWorldHint=True,
    ),
)(buscar_discrepancias)

mcp.tool(
    title="Leer documento del Panel de Expertos",
    annotations=ToolAnnotations(
        title="Leer documento del Panel de Expertos",
        readOnlyHint=True,
        destructiveHint=False,
        openWorldHint=True,
    ),
)(leer_documento)


@mcp.custom_route("/", methods=["GET"])
async def _inicio(request: Request) -> HTMLResponse:
    return HTMLResponse(pagina_inicio(BASE))


@mcp.custom_route("/privacy", methods=["GET"])
async def _privacidad(request: Request) -> HTMLResponse:
    return HTMLResponse(pagina_privacidad(BASE, CONTACTO))


@mcp.custom_route("/terms", methods=["GET"])
async def _terminos(request: Request) -> HTMLResponse:
    return HTMLResponse(pagina_terminos(BASE, CONTACTO))


@mcp.custom_route("/logo.svg", methods=["GET"])
async def _logo(request: Request) -> Response:
    return Response(LOGO_SVG, media_type="image/svg+xml")


@mcp.custom_route("/favicon.svg", methods=["GET"])
async def _favicon(request: Request) -> Response:
    return Response(FAVICON_SVG, media_type="image/svg+xml")


@mcp.custom_route("/favicon.ico", methods=["GET"])
async def _favicon_ico(request: Request) -> Response:
    return Response(base64.b64decode(FAVICON_ICO_B64), media_type="image/x-icon")


@mcp.custom_route("/favicon.png", methods=["GET"])
async def _favicon_png(request: Request) -> Response:
    return Response(base64.b64decode(FAVICON_PNG_B64), media_type="image/png")


@mcp.custom_route("/health", methods=["GET"])
async def _health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "panel-expertos-mcp"})


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
