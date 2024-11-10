import typing
import pydantic

class XmasException(Exception):

    def __init__(self, code: int, msg: str):
        self._code = code
        self._msg = msg


class StatusResponse(pydantic.BaseModel):
    status: int
    msg: str


class XMasFeedback(pydantic.BaseModel):
    year: int
    hasPicture: bool
    message: str


class XMasPerson(pydantic.BaseModel):
    id: str
    name: str
    language: str
    greeting: str
    feedback: typing.List[XMasFeedback] = pydantic.Field(default_factory=list)
