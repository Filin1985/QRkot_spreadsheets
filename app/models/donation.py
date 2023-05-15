from sqlalchemy import Column, Integer, Text, ForeignKey

from app.models.base import BaseModel


class Donation(BaseModel):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'{self.user_id} - {self.comment}'
            f'{super().__repr__()}'
        )
