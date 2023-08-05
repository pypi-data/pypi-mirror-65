from typing import *
from zo.pydantic import BaseModel, EmailStr, HttpUrl, validator, constr


class RespBase(BaseModel):
    message: str = 'ok'
    result: Any
    detail: dict = {}


class RespDict(RespBase):
    result: dict


class RespList(RespBase):
    result: List


class RespStr(RespBase):
    result: str


class RespInt(RespBase):
    result: int


class RespFloat(RespBase):
    result: float


def resp(result=None, **kwargs) -> RespBase:  # aa = {'message': message, 'result': result, 'detail': kwargs}
    return RespBase(result={} if result is None else result, detail=kwargs)
