import typing
import pydantic

class XMasException(Exception):

    def __init__(self, code: int, msg: str):
        self._code = code
        self._msg = msg

    @property
    def code(self) -> int:
        return self._code

    @property
    def msg(self) -> str:
        return self._msg

    def __repr__(self) -> str:
        return f"XMasException(code={self._code}, msg={self._msg})"

class StatusResponse(pydantic.BaseModel):
    status: int
    msg: str

class XMasFeedback(pydantic.BaseModel):
    year: int = pydantic.Field(default=2024)
    hasPicture: bool = pydantic.Field(default=False)
    message: str = pydantic.Field(default='')

class XMasPerson(pydantic.BaseModel):
    type: str = pydantic.Field(default='XMasPerson')
    id: str = pydantic.Field(default='0')
    name: str = pydantic.Field(default='Stranger')
    language: str = pydantic.Field(default='en')
    greeting: str = pydantic.Field(default='Merry Christmas')
    eligibleForCurrentYear: bool = pydantic.Field(default=False)
    feedback: typing.List[XMasFeedback] = pydantic.Field(default_factory=list)

class XMas2024Person(pydantic.BaseModel):
    id: str
    name: str
    language: str
    greeting: str
    hasPicture: bool = pydantic.Field(default=False)
    message: str = pydantic.Field(default="")

    @staticmethod
    def from_xmas_person(xmas_person: XMasPerson) -> 'XMas2024Person':
        xmas_2024_person = XMas2024Person(
            id=xmas_person.id,
            name=xmas_person.name,
            language=xmas_person.language,
            greeting=xmas_person.greeting)
        feedback2024 = list(filter(lambda f: f.year == 2024, xmas_person.feedback))
        if len(feedback2024) != 0:
            xmas_2024_person.hasPicture = feedback2024[0].hasPicture
            xmas_2024_person.message = feedback2024[0].message
        return xmas_2024_person

class XMas2024Feedback(pydantic.BaseModel):
    message: str = pydantic.Field(default='')
