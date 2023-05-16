from http import HTTPStatus
from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api import (
    spreadsheets_create, set_user_permissions, spreadsheets_update_value
)


ERROR_MESSAGE = 'Запрос с текущими параметрами невозможно испольнить'
DOCS_URL = 'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'


router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_project_crud.get_projects_by_fully_invested(
        session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            projects,
            wrapper_services
        )
    except ValueError:
        raise HTTPStatus(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ERROR_MESSAGE
        )
    return {'url': DOCS_URL.format(spreadsheet_id=spreadsheet_id)}
