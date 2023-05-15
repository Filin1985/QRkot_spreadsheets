from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


PROJECT_EXIST_ERROR = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND_ERROR = 'Проект с id {project_id} не найден!'
INVESTED_AMOUNT_ERROR = 'В проект были внесены средства, не подлежит удалению!'
NEW_AMOUNT_ERROR = 'Новая сумма проекта недолжна быть меньше внесенной!'
INVESTED_PROJECT_ERROR = 'Закрытый проект нельзя редактировать!'
CLOSED_PROJECT_ERROR = 'Закрытый проект удалить нельзя!'


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    name_id = await charity_project_crud.get_project_id_by_name(name, session)
    if name_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_EXIST_ERROR,
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND_ERROR.format(project_id=project_id)
        )
    return project


def check_project_invested_amount(project: CharityProject):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVESTED_AMOUNT_ERROR
        )


def check_full_amount(project: CharityProject, new_amount: int):
    if new_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NEW_AMOUNT_ERROR
        )


def check_project_invested(project: CharityProject):
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVESTED_PROJECT_ERROR
        )


def check_project_closed(project: CharityProject):
    if project.close_date and project.close_date < datetime.now():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CLOSED_PROJECT_ERROR
        )
