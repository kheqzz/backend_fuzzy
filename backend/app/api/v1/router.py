"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import user,iot


api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(iot.router, prefix="/iot", tags=["iot"])

