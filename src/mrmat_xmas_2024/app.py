import typing
import os
import pathlib
import contextlib

import fastapi
import fastapi.middleware.cors
import fastapi.staticfiles
import azure.identity
import pydantic
import azure.cosmos
import azure.cosmos.exceptions
import azure.storage.blob

from mrmat_xmas_2024 import __version__, __version_header__, __default_config_file__
from mrmat_xmas_2024.config import Config
from mrmat_xmas_2024.model import (
    XMasException,
    StatusResponse,
    XMasPerson, XMasFeedback,
    XMas2024Person, XMas2024Feedback )

config = Config(__default_config_file__)
app_credential = azure.identity.DefaultAzureCredential()
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
    raw_uids: typing.List[typing.Dict[str, str]] = cosmos_container_client.query_items(
        query='SELECT c.id FROM c WHERE c.eligibleForCurrentYear = true',
        enable_cross_partition_query=True)
    for uid in raw_uids:
        known_uids.append(uid.get('id'))
    yield

app = fastapi.FastAPI(
    lifespan=lifespan
)
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=['https://mrmat-xmas.azurewebsites.net', 'http://localhost:8000', 'http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['*'],
)

@app.middleware('common-headers')
async def add_common_headers(request: fastapi.Request, call_next):
    response = await call_next(request)
    response.headers[__version_header__] = __version__
    return response

@app.exception_handler(XMasException)
async def xmas_exception_handler(request: fastapi.Request, exc: XMasException):
    del request
    return fastapi.responses.JSONResponse(status_code=exc.code,
                                          content=dict(code=exc.code, msg=exc.msg))

def validate_user(uid: str) -> XMasPerson:
    try:
        if not uid in known_uids:
            raise XMasException(code=403, msg='Provided uid is not known')
        raw_person = cosmos_container_client.read_item(item=uid, partition_key=uid)
        return XMasPerson.model_validate(raw_person)
    except azure.cosmos.exceptions.CosmosHttpResponseError as chre:
        raise XMasException(code=500, msg='Failed to communicate with user store') from chre
    except pydantic.ValidationError as ve:
        raise XMasException(code=500, msg='Failed to parse response from user store') from ve


@app.get('/api/healthz', response_model=StatusResponse)
async def healthz():
    return StatusResponse(status=200, msg='OK')


@app.get('/api/people/{uid:str}',
         summary='Get user info',
         response_model=XMas2024Person)
async def user_get(caller: typing.Annotated[XMasPerson, fastapi.Depends(validate_user)]):
    return XMas2024Person.from_xmas_person(caller)


@app.post('/api/people/{uid:str}',
          summary='Update user info',
          response_model=XMas2024Person)
async def user_update(caller: typing.Annotated[XMasPerson, fastapi.Depends(validate_user)],
                      update: XMas2024Feedback):
    found = False
    for fb in caller.feedback:
        if fb.year == 2024:
            fb.message = update.message
            found = True
    if not found:
        caller.feedback.append(XMasFeedback(message=update.message))
    updated_person = cosmos_container_client.upsert_item(body=caller.model_dump())
    return XMas2024Person.from_xmas_person(XMasPerson.model_validate(updated_person))


@app.get('/api/pictures/{uid:str}',
         summary='Get the user picture, if present')
async def picture_get(caller: typing.Annotated[XMasPerson, fastapi.Depends(validate_user)]) -> fastapi.Response:
    with container_client.get_blob_client(f'2024/${caller.id}') as blob_client:
        if not blob_client.exists():
            raise fastapi.HTTPException(status_code=404, detail='Sorry, I have no picture for you')
        media = blob_client.get_blob_properties().get('content_settings', {}).get('content_type')
        if media is None:
            raise fastapi.HTTPException(status_code=500, detail='Invalid content type for the picture')
        content = blob_client.download_blob().readall()
    return fastapi.Response(content=content, media_type=media)


@app.post('/api/pictures/{uid}',
          summary='Update the user picture',
          response_model=XMas2024Person)
async def picture_update(caller: typing.Annotated[XMasPerson, fastapi.Depends(validate_user)],
                         file: typing.Annotated[fastapi.UploadFile, fastapi.File(description='User picture')]):
    if file.content_type not in __content_type_map__.keys():
        raise fastapi.HTTPException(status_code=400, detail='You must upload a jpeg or png image')
    with container_client.get_blob_client(f'2024/{caller.id}') as blob_client:
        content = file.file.read()
        blob_client.upload_blob(data=content,
                                overwrite=True,
                                content_settings=azure.storage.blob.ContentSettings(content_type=file.content_type))
    found = False
    for fb in caller.feedback:
        if fb.year == 2024:
            fb.hasPicture = True
            found = True
    if not found:
        caller.feedback.append(XMasFeedback(hasPicture=True))
    updated_person = cosmos_container_client.upsert_item(body=caller.model_dump())
    return XMas2024Person.from_xmas_person(XMasPerson.model_validate(updated_person))

class SPAStaticFilesWithFallback(fastapi.staticfiles.StaticFiles):
    """
    An override for static files to fall back to the index if the relative path has not been found.
    This permits us to serve an SPA from a single webapp.
    """

    def __init__(self, directory: os.PathLike, index='index.html'):
        self.index = index
        super().__init__(directory=directory, html=True, check_dir=True)

    def lookup_path(self, path: str) -> typing.Tuple[str, typing.Optional[os.stat_result]]:
        full_path, stat_result = super().lookup_path(path)
        if not stat_result:
            return super().lookup_path(self.index)
        return full_path, stat_result


app.mount(path='/',
          app=SPAStaticFilesWithFallback(directory=pathlib.Path(os.path.dirname(__file__), 'static')),
          name='static')