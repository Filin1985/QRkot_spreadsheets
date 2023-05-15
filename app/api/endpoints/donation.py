from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationResponse
)
from app.services.invest import investment_process


router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationResponse,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create(
        donation, session, False, user
    )
    project_invest = await charity_project_crud.get_open_objects(
        session
    )
    invested_objects = investment_process(new_donation, project_invest)
    session.add_all(invested_objects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationResponse],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_user_donations_from_db(user, session)
