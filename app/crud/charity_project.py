from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):
    async def update_charity_project(
            self,
            db_project: CharityProject,
            project_in: CharityProjectUpdate,
            session: AsyncSession
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_project)
        update_data = project_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_project, field, update_data[field])
        if db_project.full_amount == db_project.invested_amount:
            db_project.fully_invested = True
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project

    async def get_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return db_project.scalars().first()
    
    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> List[CharityProject]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            )
        )
        return sorted(
            projects.scalars().all(),
            key=lambda project: project.close_date - project.create_date
        )


charity_project_crud = CRUDCharityProject(CharityProject)
