from pydantic import BaseModel


class BaseModelValidation(BaseModel):
    class Config:
        validate_assignment = True


class BaseModelWithoutValidation(BaseModel):  # same as BaseModel
    class Config:
        validate_assignment = False  # default
