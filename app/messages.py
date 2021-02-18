"""Friendly messsages"""

from fastapi import APIRouter

router = APIRouter()

@router.get('/user/{name}')
async def hello(name: str):
    """Returns a friendly greeting 👋"""
    return {'message': f'What up {name}'}