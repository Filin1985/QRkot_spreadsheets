from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra, validator

NAME_NULL_MESSAGE = 'Название проекта не может быть пустым!'
MIN_LENGTH_PROJECT = 1
MAX_LENGTH_PROJECT = 100
MORE_AMOUNT_PROJECT = 0


class CharityProjectUpdate(BaseModel):
    name: str = Field(
        None,
        min_length=MIN_LENGTH_PROJECT,
        max_length=MAX_LENGTH_PROJECT)
    description: str = Field(None, min_length=MIN_LENGTH_PROJECT)
    full_amount: int = Field(None, gt=MORE_AMOUNT_PROJECT)

    class Config:
        extra = Extra.forbid

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(NAME_NULL_MESSAGE)
        return value


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(
        ...,
        min_length=MIN_LENGTH_PROJECT,
        max_length=MAX_LENGTH_PROJECT
    )
    description: str = Field(..., min_length=MIN_LENGTH_PROJECT)
    full_amount: int = Field(..., gt=MORE_AMOUNT_PROJECT)


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
        validate_assignment = True

    @validator('invested_amount')
    def set_invested_amount(cls, invested_amount):
        return invested_amount or 0

    @validator('fully_invested')
    def set_fully_invested(cls, fully_invested):
        return fully_invested or False
