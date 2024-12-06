from fastapi import APIRouter, Depends


router = APIRouter(prefix='/setup', tags=['Setup'])


async def create_service():
        pass