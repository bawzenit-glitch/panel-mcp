"""
Páginas públicas del conector Panel de Expertos: producto (/), privacidad
(/privacy) y términos (/terms). URLs estables servidas por el servidor.
"""

from datetime import date

_FECHA = date.today().strftime("%d/%m/%Y")

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Panel de Expertos">
  <defs>
    <linearGradient id="wing" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#d9ccff"/><stop offset="0.5" stop-color="#a78bfa"/><stop offset="1" stop-color="#7c3aed"/>
    </linearGradient>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#c4b5fd"/><stop offset="1" stop-color="#6d28d9"/>
    </linearGradient>
    <g id="wingset" stroke="#2a1a5e" stroke-width="5" stroke-linejoin="round">
      <g transform="translate(252,292) rotate(-74)"><ellipse cx="118" cy="0" rx="118" ry="32" fill="url(#wing)"/><ellipse cx="150" cy="-9" rx="46" ry="11" fill="#ece7ff" opacity="0.55" stroke="none"/></g>
      <g transform="translate(252,292) rotate(-50)"><ellipse cx="138" cy="0" rx="138" ry="36" fill="url(#wing)"/><ellipse cx="176" cy="-11" rx="54" ry="12" fill="#ece7ff" opacity="0.55" stroke="none"/></g>
      <g transform="translate(252,292) rotate(-22)"><ellipse cx="122" cy="0" rx="122" ry="30" fill="url(#wing)"/><ellipse cx="156" cy="-9" rx="48" ry="10" fill="#ece7ff" opacity="0.5" stroke="none"/></g>
      <g transform="translate(252,300) rotate(16)"><ellipse cx="96" cy="0" rx="96" ry="26" fill="url(#wing)"/><ellipse cx="120" cy="-7" rx="38" ry="9" fill="#ece7ff" opacity="0.5" stroke="none"/></g>
      <g transform="translate(252,300) rotate(42)"><ellipse cx="72" cy="0" rx="72" ry="21" fill="url(#wing)"/><ellipse cx="92" cy="-6" rx="28" ry="7" fill="#ece7ff" opacity="0.45" stroke="none"/></g>
    </g>
  </defs>
  <rect width="512" height="512" rx="112" fill="#120b25"/>
  <use href="#wingset"/>
  <use href="#wingset" transform="translate(512,0) scale(-1,1)"/>
  <g fill="none" stroke="#4a3a86" stroke-width="6" stroke-linecap="round">
    <path d="M246 252 C234 220 228 206 222 196"/><path d="M266 252 C278 220 284 206 290 196"/>
  </g>
  <circle cx="222" cy="194" r="7" fill="#c4b5fd"/><circle cx="290" cy="194" r="7" fill="#c4b5fd"/>
  <circle cx="256" cy="266" r="20" fill="url(#body)" stroke="#2a1a5e" stroke-width="5"/>
  <circle cx="248" cy="262" r="6" fill="#ece7ff"/><circle cx="264" cy="262" r="6" fill="#ece7ff"/>
  <path d="M256 280 C288 292 288 360 256 408 C224 360 224 292 256 280 Z" fill="url(#body)" stroke="#2a1a5e" stroke-width="5"/>
  <path d="M250 300 C246 330 248 360 256 392" fill="none" stroke="#ece7ff" stroke-width="7" stroke-linecap="round" opacity="0.6"/>
</svg>"""

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="Panel de Expertos">
  <defs>
    <linearGradient id="w" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9ccff"/><stop offset="1" stop-color="#7c3aed"/></linearGradient>
    <g id="fw" stroke="#2a1a5e" stroke-width="1.4" stroke-linejoin="round">
      <g transform="translate(32,34) rotate(-62)"><ellipse cx="16" cy="0" rx="16" ry="5.2" fill="url(#w)"/></g>
      <g transform="translate(32,34) rotate(-34)"><ellipse cx="18.5" cy="0" rx="18.5" ry="5.6" fill="url(#w)"/></g>
      <g transform="translate(32,35) rotate(-6)"><ellipse cx="15.5" cy="0" rx="15.5" ry="4.6" fill="url(#w)"/></g>
      <g transform="translate(32,36) rotate(26)"><ellipse cx="11" cy="0" rx="11" ry="3.6" fill="url(#w)"/></g>
    </g>
  </defs>
  <rect width="64" height="64" rx="16" fill="#120b25"/>
  <use href="#fw"/><use href="#fw" transform="translate(64,0) scale(-1,1)"/>
  <circle cx="32" cy="31" r="3" fill="url(#w)" stroke="#2a1a5e" stroke-width="1.2"/>
  <path d="M32 33 C36 38 36 47 32 53 C28 47 28 38 32 33 Z" fill="url(#w)" stroke="#2a1a5e" stroke-width="1.2"/>
</svg>"""

_ESTILO = """
<style>
  :root { color-scheme: light dark; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
         line-height: 1.6; max-width: 760px; margin: 0 auto; padding: 40px 24px;
         color: #1a1a1a; background: #fff; }
  h1 { font-size: 1.9rem; margin-bottom: .2em; }
  h2 { font-size: 1.2rem; margin-top: 1.8em; }
  .sub { color: #666; font-size: 1.05rem; margin-top: 0; }
  code { background: #f1f1f3; padding: 2px 6px; border-radius: 5px; font-size: .92em; }
  .pill { display:inline-block; background:#2440b0; color:#fff; font-size:.75rem;
          padding:3px 10px; border-radius:999px; vertical-align:middle; }
  .card { border:1px solid #e3e3e7; border-radius:12px; padding:18px 22px; margin:18px 0; }
  a { color:#1c4fd6; }
  footer { margin-top:3em; padding-top:1.2em; border-top:1px solid #eee; color:#888; font-size:.9rem; }
  ul { padding-left: 1.2em; }
</style>
"""

_HEAD = """<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon.png">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">"""


def pagina_inicio(base_url: str) -> str:
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
{_HEAD}
<title>Conector Panel de Expertos para Claude</title>{_ESTILO}</head><body>
<img src="/logo.svg" alt="Panel de Expertos" width="96" height="96"
     style="display:block;border-radius:22px;margin-bottom:14px"/>
<h1>Conector Panel de Expertos <span class="pill">MCP</span></h1>
<p class="sub">Consulta las discrepancias del mercado eléctrico chileno resueltas
por el Panel de Expertos, directamente desde Claude.</p>

<p>Este conector permite que Claude busque discrepancias tramitadas por el
<a href="https://panelexpertos.cl">Panel de Expertos</a> en lenguaje natural:
por partes involucradas (empresas, CNE, Coordinador), materia, número o año.
Devuelve el número de discrepancia, las partes, la materia, el año y el enlace al
expediente con sus documentos.</p>

<h2>Qué puede hacer</h2>
<ul>
  <li><strong>Buscar discrepancias</strong> por texto libre (partes, materia,
      número), con filtro opcional por año.</li>
  <li><strong>Incluir documentos</strong> de cada discrepancia, con enlace en
      SharePoint y URL de descarga.</li>
</ul>

<h2>Cómo conectarlo</h2>
<div class="card">
  En Claude: <em>Configuración → Conectores → Agregar conector personalizado</em>,
  y pega esta URL:<br><br>
  <code>{base_url}/mcp</code>
</div>

<h2>Ejemplos</h2>
<ul>
  <li><em>"Busca discrepancias sobre peajes de distribución."</em></li>
  <li><em>"Discrepancias de Engie contra la CNE en 2024."</em></li>
  <li><em>"Discrepancias por acceso abierto a la transmisión, incluye documentos."</em></li>
</ul>

<h2>Solución de problemas</h2>
<ul>
  <li><strong>No conecta:</strong> verifica que la URL termine en <code>/mcp</code>
      y deja vacíos los campos de OAuth.</li>
  <li><strong>Pide volver a autorizar:</strong> reconéctalo desde Configuración →
      Conectores.</li>
  <li><strong>Sin resultados:</strong> usa términos más generales (nombre de una
      parte o de la materia) o quita el filtro de año.</li>
  <li>¿Otro problema? Escríbenos a
      <a href="mailto:contacto@bfly-cluster.ai">contacto@bfly-cluster.ai</a>.</li>
</ul>

<h2>Aviso</h2>
<p>Servicio independiente desarrollado por Orko. <strong>No está afiliado ni
respaldado por el Panel de Expertos ni por el Gobierno de Chile.</strong> Consulta
y expone información pública del sitio del Panel (panelexpertos.cl) conforme a la
Ley 20.285 de transparencia.</p>

<footer>
  Desarrollado por <strong>Orko</strong> ·
  <a href="mailto:contacto@bfly-cluster.ai">contacto@bfly-cluster.ai</a><br><br>
  Datos: Panel de Expertos del mercado eléctrico de Chile (información pública,
  Ley 20.285). &nbsp;·&nbsp;
  <a href="{base_url}/privacy">Política de privacidad</a> &nbsp;·&nbsp;
  <a href="{base_url}/terms">Términos de servicio</a>
</footer>
</body></html>"""


def pagina_privacidad(base_url: str, contacto: str) -> str:
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
{_HEAD}
<title>Política de privacidad — Conector Panel de Expertos</title>{_ESTILO}</head><body>
<h1>Política de privacidad</h1>
<p class="sub">Conector Panel de Expertos para Claude · Última actualización: {_FECHA}</p>

<p>Esta política describe cómo el conector (en adelante, "el conector") trata la
información cuando se usa con Claude u otros clientes compatibles con MCP.</p>

<h2>1. Qué información se procesa</h2>
<ul>
  <li><strong>Consultas:</strong> el texto de búsqueda que envías se usa
      únicamente para consultar el buscador público del Panel de Expertos y
      devolverte el resultado.</li>
  <li><strong>Registros de uso (logs):</strong> el servidor registra metadatos
      operativos (herramienta usada, términos de la consulta y marca de tiempo)
      con fines de funcionamiento y diagnóstico. No contienen datos personales.</li>
  <li><strong>No se solicitan ni almacenan datos personales</strong>; el conector
      no requiere crear una cuenta.</li>
</ul>

<h2>2. Autenticación</h2>
<p>El conector usa OAuth 2.1 con registro dinámico de clientes (requisito de
Claude para conectores remotos). La autorización es automática: se emiten tokens
anónimos y temporales, no asociados a ninguna identidad personal.</p>

<h2>3. Origen de los datos</h2>
<p>La información proviene del sitio público del Panel de Expertos
(<a href="https://panelexpertos.cl">panelexpertos.cl</a> y su buscador), que es
información pública conforme a la Ley 20.285 de transparencia. El conector no
genera ni modifica datos del Panel.</p>

<h2>4. Uso compartido</h2>
<p>El conector no vende ni comparte información con terceros. Las consultas se
dirigen exclusivamente al buscador del Panel para obtener el resultado.</p>

<h2>5. Retención</h2>
<p>Los registros de uso son efímeros y se conservan solo el tiempo necesario para
la operación y el diagnóstico. No se construyen perfiles de usuario.</p>

<h2>6. Seguridad</h2>
<p>El acceso a las herramientas requiere completar el flujo OAuth descrito.</p>

<h2>7. Contacto</h2>
<p>Conector desarrollado por <strong>Orko</strong>. Consultas:
<a href="mailto:{contacto}">{contacto}</a>.</p>

<footer><a href="{base_url}/">← Volver al inicio</a> &nbsp;·&nbsp;
<a href="{base_url}/terms">Términos de servicio</a></footer>
</body></html>"""


def pagina_terminos(base_url: str, contacto: str) -> str:
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
{_HEAD}
<title>Términos de servicio — Conector Panel de Expertos</title>{_ESTILO}</head><body>
<h1>Términos de servicio</h1>
<p class="sub">Conector Panel de Expertos para Claude · Última actualización: {_FECHA}</p>

<p>Al usar el conector (en adelante, "el servicio") aceptas estos términos.</p>

<h2>1. Descripción</h2>
<p>El servicio permite consultar información pública de las discrepancias del
mercado eléctrico chileno resueltas por el Panel de Expertos, a través de Claude.
Es de solo lectura: no crea, modifica ni elimina datos.</p>

<h2>2. Sin afiliación oficial</h2>
<p>Servicio desarrollado de forma independiente por <strong>Orko</strong>.
<strong>No está afiliado, asociado ni respaldado por el Panel de Expertos ni por
el Gobierno de Chile.</strong> La información proviene del sitio público
<a href="https://panelexpertos.cl">panelexpertos.cl</a>, conforme a la Ley 20.285
de transparencia.</p>

<h2>3. Uso aceptable</h2>
<p>Debes usar el servicio de forma razonable y conforme a la ley, sin intentar
sobrecargarlo ni vulnerar su seguridad.</p>

<h2>4. "Tal cual"</h2>
<p>El servicio se ofrece "tal cual", sin garantías de disponibilidad, exactitud o
continuidad. La información depende del sitio del Panel y puede cambiar. Para
fines oficiales, verifica siempre en panelexpertos.cl.</p>

<h2>5. Limitación de responsabilidad</h2>
<p>En la máxima medida permitida por la ley, el desarrollador no será responsable
por daños derivados del uso o la imposibilidad de uso del servicio.</p>

<h2>6. Cambios</h2>
<p>Estos términos pueden actualizarse. El uso continuado implica su aceptación.</p>

<h2>7. Contacto</h2>
<p>Consultas: <a href="mailto:{contacto}">{contacto}</a>.</p>

<footer><a href="{base_url}/">← Volver al inicio</a> &nbsp;·&nbsp;
<a href="{base_url}/privacy">Política de privacidad</a></footer>
</body></html>"""
