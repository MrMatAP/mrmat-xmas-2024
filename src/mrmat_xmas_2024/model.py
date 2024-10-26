import pydantic

class XmasException(Exception):

    def __init__(self, code: int, msg: str):
        self._code = code
        self._msg = msg


class StatusResponse(pydantic.BaseModel):
    status: int
    msg: str
