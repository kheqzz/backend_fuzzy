from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import get_user_service, get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.core.security import get_password_hash, create_access_token
from app.core.exceptions import UserNotFoundError as ex,UnauthorizedError, EntityNotFoundError
from app.models.user import User
from app.schemas.user import TokenResponse, UserCreate, UserOut, UserUpdate
from app.db.dependencies import get_async_session
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_async_session),
):
    """Create a new user."""
    
    user = await user_service.create_user(user_in, db)
    return user

@router.post("/login", response_model=TokenResponse)
async def login_user(user_form: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(get_user_service), db: AsyncSession = Depends(get_async_session)):
    """Authenticate a user and return their details."""
    # This endpoint should be implemented to handle login logic.
    user = await user_service.login_user(
        username=user_form.username, email=None, password=user_form.password, db=db)
    if not user:
        raise UnauthorizedError(message="Could not validate credentials")

    access_token = create_access_token(secrets={"sub": str(user.id)})
   
        
    return TokenResponse(access_token=access_token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Get the current authenticated user."""
    return current_user

@router.get("/", response_model=list[UserOut])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session),
    user_service: UserService = Depends(get_user_service)
):
    """Retrieve list of users."""
    
    return await user_service.get_all_user(db)


@router.get("/{user_id}", response_model=UserOut)
async def read_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    user_service: UserService = Depends(get_user_service)
):
    """Get a user by UUID."""
    user = await user_service.get_user_by_id(user_id, db)
    if user is None:
        raise EntityNotFoundError(entity_name="User", entity_id=user_id)
    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Update a user."""
    
    return await user_service.update_user(user_id, user_in, db)


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Delete a user."""
    success = await user_service.delete_user(user_id, db)
    if not success:
        return {"message": "User not found"}
    return {"message": "User deleted successfully"}