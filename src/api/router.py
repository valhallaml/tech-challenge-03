from fastapi import APIRouter
from api.v1.football import router

api_router = APIRouter()
api_router.include_router(router, prefix='/football', tags=[ 'football' ])
