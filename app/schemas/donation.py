from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Extra, Field, PositiveInt


EXAMPLE_DONATION = 'Решил инвестировать деньги в ваши проекты.'
EXAMPLE_AMOUNT = 1000


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(
        ...,
        example=EXAMPLE_AMOUNT
    )
    comment: Union[None, str] = Field(
        None,
        example=EXAMPLE_DONATION
    )

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationResponse(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationResponse):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
