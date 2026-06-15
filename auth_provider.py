"""
Proveedor OAuth 2.1 de auto-aprobación para el conector SEIA remoto, con
PERSISTENCIA en disco para que el estado (clientes, tokens) sobreviva a
reinicios del servidor.

¿Por qué existe? Claude exige que los conectores remotos hablen OAuth con
registro dinámico de clientes (DCR). Como los datos del SEIA son públicos, no
necesitamos cuentas ni login: este proveedor completa el "baile" OAuth que
Claude requiere y le entrega un token a cualquiera que complete el flujo.

Persistencia: el estado se guarda en un archivo JSON. La ruta se toma de:
  1. SEIA_DATA_DIR (si se define), o
  2. RAILWAY_VOLUME_MOUNT_PATH (si hay un Volume montado en Railway), o
  3. el directorio actual (fallback; en Railway sin Volume esto se borra en
     cada redeploy, pero sobrevive a reinicios dentro del mismo despliegue).
Para persistencia total entre redeploys en Railway: agregar un Volume al
servicio (el código lo detecta solo).

Si más adelante quieres control de acceso real (saber quién es cada usuario,
cobrar, etc.), este es el punto donde se agregaría un login/verificación antes
de emitir el código en `authorize()`.
"""

import json
import os
import secrets
import time

from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    RefreshToken,
    construct_redirect_uri,
)
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

_VIDA_CODIGO = 300       # segundos de validez del authorization code
_VIDA_TOKEN = 3600       # segundos de validez del access token


def _ruta_estado() -> str:
    base = (
        os.environ.get("SEIA_DATA_DIR")
        or os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
        or os.path.dirname(os.path.abspath(__file__))
    )
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "oauth_state.json")


class ProveedorOAuthAutoAprobacion:
    """Implementa OAuthAuthorizationServerProvider con auto-aprobación y
    persistencia en disco."""

    def __init__(self) -> None:
        self._archivo = _ruta_estado()
        self._clientes: dict[str, OAuthClientInformationFull] = {}
        self._codigos: dict[str, AuthorizationCode] = {}
        self._tokens: dict[str, AccessToken] = {}
        self._refresh: dict[str, RefreshToken] = {}
        self._cargar()

    # --- Persistencia ------------------------------------------------------
    def _cargar(self) -> None:
        try:
            with open(self._archivo, encoding="utf-8") as f:
                d = json.load(f)
            self._clientes = {
                k: OAuthClientInformationFull.model_validate(v)
                for k, v in d.get("clientes", {}).items()
            }
            self._codigos = {
                k: AuthorizationCode.model_validate(v)
                for k, v in d.get("codigos", {}).items()
            }
            self._tokens = {
                k: AccessToken.model_validate(v)
                for k, v in d.get("tokens", {}).items()
            }
            self._refresh = {
                k: RefreshToken.model_validate(v)
                for k, v in d.get("refresh", {}).items()
            }
        except (OSError, ValueError, KeyError):
            # Archivo inexistente o corrupto: se empieza vacío (igual que antes).
            pass

    def _guardar(self) -> None:
        try:
            d = {
                "clientes": {k: v.model_dump(mode="json") for k, v in self._clientes.items()},
                "codigos": {k: v.model_dump(mode="json") for k, v in self._codigos.items()},
                "tokens": {k: v.model_dump(mode="json") for k, v in self._tokens.items()},
                "refresh": {k: v.model_dump(mode="json") for k, v in self._refresh.items()},
            }
            tmp = self._archivo + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(d, f)
            os.replace(tmp, self._archivo)  # escritura atómica
        except OSError:
            # No se pudo guardar: el servicio sigue funcionando en memoria.
            pass

    # --- Registro dinámico de clientes (DCR) --------------------------------
    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        return self._clientes.get(client_id)

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        self._clientes[client_info.client_id] = client_info
        self._guardar()

    # --- Autorización (auto-aprobada, sin login) ----------------------------
    async def authorize(
        self, client: OAuthClientInformationFull, params: AuthorizationParams
    ) -> str:
        codigo = secrets.token_hex(32)  # 256 bits de entropía
        self._codigos[codigo] = AuthorizationCode(
            code=codigo,
            scopes=params.scopes or [],
            expires_at=time.time() + _VIDA_CODIGO,
            client_id=client.client_id,
            code_challenge=params.code_challenge,
            redirect_uri=params.redirect_uri,
            redirect_uri_provided_explicitly=params.redirect_uri_provided_explicitly,
            resource=params.resource,
        )
        self._guardar()
        return construct_redirect_uri(
            str(params.redirect_uri), code=codigo, state=params.state
        )

    async def load_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: str
    ) -> AuthorizationCode | None:
        ac = self._codigos.get(authorization_code)
        if ac and ac.client_id == client.client_id and ac.expires_at >= time.time():
            return ac
        return None

    async def exchange_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: AuthorizationCode
    ) -> OAuthToken:
        self._codigos.pop(authorization_code.code, None)
        return self._emitir(
            client.client_id, authorization_code.scopes, authorization_code.resource
        )

    # --- Refresh tokens -----------------------------------------------------
    async def load_refresh_token(
        self, client: OAuthClientInformationFull, refresh_token: str
    ) -> RefreshToken | None:
        rt = self._refresh.get(refresh_token)
        if rt and rt.client_id == client.client_id:
            return rt
        return None

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: RefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        self._refresh.pop(refresh_token.token, None)  # rotación
        return self._emitir(
            client.client_id, scopes or refresh_token.scopes, None
        )

    # --- Verificación / revocación de tokens --------------------------------
    async def load_access_token(self, token: str) -> AccessToken | None:
        at = self._tokens.get(token)
        if at and (at.expires_at is None or at.expires_at >= time.time()):
            return at
        return None

    async def revoke_token(self, token) -> None:
        t = getattr(token, "token", None)
        if t:
            self._tokens.pop(t, None)
            self._refresh.pop(t, None)
            self._guardar()

    # --- Helper interno -----------------------------------------------------
    def _emitir(self, client_id: str, scopes: list[str], resource) -> OAuthToken:
        access = secrets.token_hex(32)
        refresh = secrets.token_hex(32)
        ahora = int(time.time())
        self._tokens[access] = AccessToken(
            token=access,
            client_id=client_id,
            scopes=scopes or [],
            expires_at=ahora + _VIDA_TOKEN,
            resource=resource,
        )
        self._refresh[refresh] = RefreshToken(
            token=refresh,
            client_id=client_id,
            scopes=scopes or [],
        )
        self._guardar()
        return OAuthToken(
            access_token=access,
            token_type="Bearer",
            expires_in=_VIDA_TOKEN,
            refresh_token=refresh,
            scope=" ".join(scopes) if scopes else None,
        )
