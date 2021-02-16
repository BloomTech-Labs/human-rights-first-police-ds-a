"""Friendly messsages"""

from fastapi import APIRouter

router = APIRouter()


@router.get('/users/{name}')
async def hello(name: str):
    """Returns a friendly greeting 👋"""
    return {'message': f'What up {name}'}
    # return {"messsage": "What up dog!"}