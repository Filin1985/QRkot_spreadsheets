from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_name_duplicate,
    check_project_invested_amount,
    check_full_amount,
    check_project_invested,
    check_project_closed
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.invest import investment_process


router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project, session, False
    )
    session.add_all(investment_process(
        new_project,
        await donation_crud.get_open_objects(session)
    ))
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_charity_project_exists(
        project_id, session
    )
    await check_name_duplicate(obj_in.name, session)
    check_project_invested(project)
    if obj_in.name is not None:
        await charity_project_crud.get_project_id_by_name(obj_in.name, session)
    if obj_in.full_amount:
        check_full_amount(project, obj_in.full_amount)
    project = await charity_project_crud.update_charity_project(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    project = await check_charity_project_exists(
        project_id, session
    )
    check_project_closed(project)
    check_project_invested_amount(project)
    return await charity_project_crud.remove(
        project, session
    )
