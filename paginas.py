"""
Páginas públicas del conector Panel de Expertos: producto (/), privacidad
(/privacy) y términos (/terms). URLs estables servidas por el servidor.
"""

from datetime import date

_FECHA = date.today().strftime("%d/%m/%Y")

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Panel de Expertos">
  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#3b5bdb"/><stop offset="1" stop-color="#1c2f86"/>
  </linearGradient></defs>
  <rect width="512" height="512" rx="112" fill="url(#bg)"/>
  <g stroke="#ffffff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <line x1="256" y1="120" x2="256" y2="372"/>
    <line x1="132" y1="158" x2="380" y2="158"/>
    <circle cx="256" cy="120" r="14" fill="#ffffff"/>
    <line x1="132" y1="158" x2="100" y2="250"/><line x1="132" y1="158" x2="164" y2="250"/>
    <path d="M88 250 a44 30 0 0 0 88 0 Z" fill="#cdd8ff"/>
    <line x1="380" y1="158" x2="348" y2="250"/><line x1="380" y1="158" x2="412" y2="250"/>
    <path d="M336 250 a44 30 0 0 0 88 0 Z" fill="#cdd8ff"/>
    <line x1="200" y1="372" x2="312" y2="372"/>
    <line x1="186" y1="398" x2="326" y2="398"/>
  </g>
</svg>"""

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="Panel de Expertos">
  <rect width="64" height="64" rx="16" fill="#2440b0"/>
  <g stroke="#ffffff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <line x1="32" y1="15" x2="32" y2="47"/><line x1="16" y1="20" x2="48" y2="20"/>
    <circle cx="32" cy="15" r="2.6" fill="#ffffff"/>
    <line x1="16" y1="20" x2="11" y2="33"/><line x1="16" y1="20" x2="21" y2="33"/>
    <path d="M9 33 a7 5 0 0 0 14 0 Z" fill="#cdd8ff"/>
    <line x1="48" y1="20" x2="43" y2="33"/><line x1="48" y1="20" x2="53" y2="33"/>
    <path d="M41 33 a7 5 0 0 0 14 0 Z" fill="#cdd8ff"/>
    <line x1="25" y1="47" x2="39" y2="47"/><line x1="23" y1="50" x2="41" y2="50"/>
  </g>
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
