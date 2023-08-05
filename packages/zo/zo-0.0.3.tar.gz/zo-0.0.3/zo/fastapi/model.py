import datetime
import re
from munch import munchify
from typing import *
from enum import Enum
from ..pydantic import BaseModel, EmailStr, HttpUrl, validator, constr, BaseModelValidation
from ..db import conn_db, DbClient
from ..aa import to_str
from .error import abort_if


class OnlyID(BaseModel):
    id: constr(min_length=1)


class EnumYesNo(str, Enum):
    yes = 'Yes'
    no = 'No'


class DateTimeModelMixin(BaseModel):
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(
            cls, value: datetime.datetime  # noqa: N805, WPS110
    ) -> datetime.datetime:
        return value or datetime.datetime.now()


class IDModelMixin(BaseModel):
    id: int = 0


class PageArgs(BaseModel):
    q: Any = ''
    page: int = 1
    page_size: int = 10


class ModelDict(BaseModelValidation):
    name: constr(min_length=1)
    key: constr(min_length=1)
    data: Any = None
    db: Any = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.db = conn_db()
        self.key = to_str(self.key)
        self.data = self.data or self.get()

    def get(self, check_flag: bool = True):
        aa = self.db.hget(self.name, self.key)
        abort_if(check_flag and not aa)
        return munchify(aa)

    def update(self, data: Any):
        self.data.update(data)

    def save(self):
        oo = self.get(False)
        if not oo or oo != self.data:
            return self.db.hset(self.name, self.key, self.data)

    def delete(self):
        return self.db.hdel(self.name, self.key)


class ModelList(BaseModelValidation):
    name: constr(min_length=1)
    ag: PageArgs = None
    data: List = None
    db: Any = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.db = conn_db()

    def get(self):
        self.data = munchify(list(self.db.hgetall(self.name).values()))
        if not self.ag:
            return self.data
        rst = []
        for i in self.data:
            if self.ag.q and not re.search(self.ag.q, str(i)):
                continue
            rst.append(i)
            if len(rst) >= self.ag.page * self.ag.page_size:
                break
        return rst[(self.ag.page - 1) * self.ag.page_size:]  # self.ag.page * self.ag.page_size


class ModelKV(BaseModelValidation):
    key: Union[List, constr(min_length=1)]
    data: Any = None
    db: Any = None
    ttl: int = None
    check_flag: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.key = to_str(self.key)
        self.db = conn_db()
        self.data = self.data or self.get()

    def get(self):
        aa = self.db.get(self.key)
        abort_if(self.check_flag and not aa)
        return aa

    def set(self, data):
        self.data = data
        if self.ttl:
            return self.db.setx(self.key, data, self.ttl)
        return self.db.set(self.key, data)

    def delete(self):
        return self.db.delete(self.key)
