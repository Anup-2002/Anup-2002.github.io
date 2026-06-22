from fastapi import APIRouter

from modules.chat_poster import verify_session

router = APIRouter()
'''
This endpoint allows users to check if they are logged in to CoinMarketCap.
It verifies the session and returns the login status.
'''

@router.get("/check-login")
def check_login():
    return verify_session()