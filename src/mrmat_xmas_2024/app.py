import fastapi
import fastapi.middleware.cors

from mrmat_xmas_2024 import __version__, __version_header__
from mrmat_xmas_2024.model import StatusResponse

app = fastapi.FastAPI(
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
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

@app.get('/api/healthz', summary='Return app health', response_model=StatusResponse)
async def healthz():
    return StatusResponse(status=200, msg='OK')
