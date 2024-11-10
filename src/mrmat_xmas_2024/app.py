import typing
import contextlib
from contextlib import asynccontextmanager
from venv import create

import fastapi
import fastapi.middleware.cors
import azure.identity
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
import azure.cosmos
import azure.storage.blob

from mrmat_xmas_2024 import __version__, __version_header__, __default_config_file__
from mrmat_xmas_2024.model import StatusResponse, XMasPerson, XMasFeedback
from mrmat_xmas_2024.config import Config

config = Config(__default_config_file__)
app_credential = azure.identity.DefaultAzureCredential()
azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    tenant_id=config.tenant_id,
    app_client_id = config.backend_client_id,
    scopes={f'api://{config.backend_client_id}/user_impersonation': 'user_impersonation'})
cosmos_client: azure.cosmos.CosmosClient = azure.cosmos.CosmosClient(
    url=config.cosmos_url,
    credential=app_credential)
cosmos_db_client = cosmos_client.get_database_client(database=config.cosmos_db)
cosmos_container_client = cosmos_db_client.get_container_client(container=config.cosmos_container)
container_client: azure.storage.blob.ContainerClient = azure.storage.blob.ContainerClient(
    account_url=config.storage_url,
    container_name=config.storage_container,
    credential=app_credential)

__content_type_map__ = {
    'image/jpeg': 'jpeg',
    'image/png': 'png',
}

known_uids: typing.List[str] = []

@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncGenerator[None, None]:
    await azure_scheme.openid_config.load_config()
    raw_uids: typing.List[typing.Dict[str, str]] = cosmos_container_client.query_items(
        query='SELECT c.id FROM c WHERE c.eligibleForCurrentYear = true',
        enable_cross_partition_query=True)
    for uid in raw_uids:
        known_uids.append(uid.get('id'))
    yield

app = fastapi.FastAPI(
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': config.backend_client_id,
        'scopes': f'api://{config.backend_client_id}/user_impersonation'
    },
    lifespan=lifespan
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

@app.get('/api/xmaspeople/{uid}')
async def identify(uid: str) -> XMasPerson:
    if not uid in known_uids:
        return XMasPerson(id='0', name='Stranger', language='en', greeting='Hello Stranger')
    raw_person = cosmos_container_client.query_items(
        query='SELECT c.id, c.name, c.language, c.greeting, c.feedback FROM c '
              'WHERE c.type = "XMasPerson" AND c.id = @uid',
        parameters=[dict(name='@uid', value=uid)])
    return XMasPerson.model_validate(next(raw_person))

@app.post('/api/xmaspeople/{uid}')
async def updateFeedback(uid: str, update: XMasFeedback) -> XMasPerson:
    if not uid in known_uids:
        raise fastapi.HTTPException(status_code=404, detail='Sorry, I do not know you')
    raw_person = cosmos_container_client.read_item(item=uid, partition_key=uid)
    if raw_person is None:
        raise fastapi.HTTPException(status_code=404, detail='Sorry, I do not know you')
    for us in ['_rid', '_self', '_etag', '_attachments', '_ts']:
        del raw_person[us]
    found = False
    for fb in raw_person.get('feedback', []):
        if fb.get('year') == 2024:
            fb['message'] = update.message
            found = True
    if not found:
        raw_person.get('feedback').append(update.model_dump())
    updated_person = cosmos_container_client.upsert_item(body=raw_person)
    return XMasPerson.model_validate(updated_person)


@app.post('/api/pictures/{uid}')
async def update_picture(uid: str,
                         file: typing.Annotated[fastapi.UploadFile, fastapi.File(description='User picture')]):
    if not uid in known_uids:
        raise fastapi.HTTPException(status_code=404, detail='Sorry, I do not know you')
    if file.content_type not in __content_type_map__.keys():
        raise fastapi.HTTPException(status_code=400, detail='You must upload a jpeg or png image')
    with container_client.get_blob_client(f'2024/${uid}') as blob_client:
        content = file.file.read()
        blob_client.upload_blob(data=content,
                                overwrite=True,
                                content_settings=azure.storage.blob.ContentSettings(content_type=file.content_type))
    raw_person = cosmos_container_client.read_item(item=uid, partition_key=uid)
    if raw_person is None:
        raise fastapi.HTTPException(status_code=404, detail='Sorry, I do not know you')
    for us in ['_rid', '_self', '_etag', '_attachments', '_ts']:
        del raw_person[us]
    found = False
    for fb in raw_person.get('feedback', []):
        if fb.get('year') == 2024:
            fb['hasPicture'] = True
            found = True
    if not found:
        raw_person.get('feedback').append(XMasFeedback(hasPicture=True).model_dump())
    updated_person = cosmos_container_client.upsert_item(body=raw_person)
    return XMasPerson.model_validate(updated_person)


@app.get('/api/pictures/{uid}')
async def get_picture(uid: str) -> fastapi.Response:
    with container_client.get_blob_client(f'2024/${uid}') as blob_client:
        if not blob_client.exists():
            raise fastapi.HTTPException(status_code=404, detail='Sorry, I have no picture for you')
        media = blob_client.get_blob_properties().get('content_settings', {}).get('content_type')
        if media is None:
            raise fastapi.HTTPException(status_code=500, detail='Invalid content type for the picture')
        content = blob_client.download_blob().readall()
    return fastapi.Response(content=content, media_type=media)

@app.get('/api/healthz', response_model=StatusResponse)
async def healthz():
    return StatusResponse(status=200, msg='OK')