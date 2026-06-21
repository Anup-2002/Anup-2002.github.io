from fastapi import APIRouter

from modules.chat_poster import verify_session

router = APIRouter()


@router.get("/check-login")
def check_login():
    return verify_session()
