from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.models import User
from src.users.service import user_service
from src.users.schemas import UserResponseSchema, UserCreateSchema, UserBaseSchema, UserPatchSchema
from src.users.dependencies import is_user_id_valid
from src.pagination import PaginationParams, PaginatedResponse

router = APIRouter()


@router.get(
    "/users",
    tags=["Users"],
    summary="Get all users",
    response_model=PaginatedResponse[UserResponseSchema],
    status_code=200)
async def get_users(db: AsyncSession = Depends(get_db),
                    pagination: PaginationParams = Depends()):
    users, total = await user_service.get_users(db, pagination)

    return PaginatedResponse.create(users, total, pagination)


@router.get(
    "/users/{user_id}",
    tags=["Users"],
    summary="Get user by id",
    response_model=UserResponseSchema,
    status_code=200)
async def get_user_by_id(
        user: User = Depends(is_user_id_valid)):
    return user


@router.post(
    "/users",
    tags=["Users"],
    summary="Create a new user",
    response_model=UserResponseSchema,
    status_code=201)
async def user_create(
        user: UserCreateSchema,
        db: AsyncSession = Depends(get_db)):
    db_user = await user_service.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await user_service.create_user(db=db, user=user)


@router.put(
    "/users/{user_id}",
    tags=["Users"],
    summary="Update the user",
    response_model=UserResponseSchema,
    status_code=200)
async def user_update(
        update_data: UserBaseSchema,
        user: User = Depends(is_user_id_valid),
        db: AsyncSession = Depends(get_db),
):
    return await user_service.update_user(db, user=user, update_data=update_data)


@router.patch(
    "/users/{user_id}",
    tags=["Users"],
    summary="PATCH the user",
    response_model=UserResponseSchema,
    status_code=200)
async def user_patch(
        update_data: UserPatchSchema,
        user: User = Depends(is_user_id_valid),
        db: AsyncSession = Depends(get_db),
):
    return await user_service.patch_user(db, user=user, update_data=update_data)


@router.delete(
    "/users/{user_id}",
    tags=["Users"],
    summary="Delete the user",
    status_code=204)
async def user_delete(
        user: User = Depends(is_user_id_valid),
        db: AsyncSession = Depends(get_db),
):
    return await user_service.delete_user(db, user=user)
