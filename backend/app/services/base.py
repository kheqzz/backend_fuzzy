from typing import Generic, TypeVar, TYPE_CHECKING, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository

#TypeVars for generic repository
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(Generic[RepositoryType]):
    """Generic service class for CRUD operations."""

    def __init__ (self, repository: RepositoryType):
        self.repository = repository

    async def get(self, db: AsyncSession, id: Any) :
        return await self.repository.get(db, id)

    async def get_all(self, db: AsyncSession) :
        return await self.repository.get_all(db)

    async def create(self, db: AsyncSession, obj_in):
        return await self.repository.create(db, obj_in)

    async def update(self, db: AsyncSession, obj_in):
        return await self.repository.update(db, obj_in)

    async def delete(self, db: AsyncSession, id: Any) :
        return await self.repository.delete(db, id)