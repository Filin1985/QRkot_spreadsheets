from sqlalchemy import Column, String, Text

from app.models.base import BaseModel


class CharityProject(BaseModel):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{self.name} - {self.description}'
            f'{super().__repr__()}'
        )
