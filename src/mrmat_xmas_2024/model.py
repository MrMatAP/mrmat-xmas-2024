import pydantic

class StatusResponse(pydantic.BaseModel):
    status: int
    msg: str
