import typing
import contextlib

import fastapi
import fastapi.middleware.cors
import azure.identity
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

from mrmat_xmas_2024 import __version__, __version_header__, __default_config_file__
from mrmat_xmas_2024.model import StatusResponse
from mrmat_xmas_2024.config import Config

config = Config(__default_config_file__)
app_credential = azure.identity.DefaultAzureCredential()
azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    tenant_id=config.tenant_id,
    app_client_id = config.backend_client_id,
    scopes={f'api://{config.backend_client_id}/user_impersonation': 'user_impersonation'}
)

app = fastapi.FastAPI(
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': config.backend_client_id,
        'scopes': f'api://{config.backend_client_id}/user_impersonation'
    }
)
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=['https://mrmat-xmas.azurewebsites.net', 'http://localhost:8000', 'http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*', 'DELETE'],
    allow_headers=['*'],
)

@app.middleware('common-headers')
async def add_common_headers(request: fastapi.Request, call_next):
    response = await call_next(request)
    response.headers[__version_header__] = __version__
    return response

@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncGenerator[None, None]:
    await azure_scheme.openid_config.load_config()
    yield

@app.get('/api/healthz', summary='Return app health', response_model=StatusResponse)
async def healthz():
    return StatusResponse(status=200, msg='OK')
