""" Twiter Data """
from fastapi import APIRouter

router =APIRouter()

@router.get('/Twitter')
async def get_Twitter_Data():
    """ Returns all twitter data from database"""
    return 'Twitter data :)'
