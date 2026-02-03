from fastapi import APIRouter, HTTPException

from src.database import DB_Session
from src.users import service
from src.users.schemas import UserResponseSchema, UserCreateSchema

router = APIRouter()


@router.get(
    "/users",
    tags=["Users"],
    summary="Get all users",
    response_model=list[UserResponseSchema],
    status_code=200)
async def get_users(db: DB_Session, skip: int = 0, limit: int = 100):
    return await service.get_users(db, skip, limit)


@router.get(
    "/users/{user_id}",
    tags=["Users"],
    summary="Get user by id",
    response_model=UserResponseSchema,
    status_code=200)
async def get_user_by_id(user_id: int, db: DB_Session):
    user = await service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post(
    "/users",
    tags=["Users"],
    summary="Create a new user",
    response_model=UserResponseSchema,
    status_code=201)
async def user_create(
        user: UserCreateSchema,
        db: DB_Session):
    db_user = await service.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await service.create_user(db=db, user=user)
