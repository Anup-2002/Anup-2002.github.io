from fastapi import APIRouter

from schemas.post import PostRequest
from modules.chat_poster import post_chat

router = APIRouter()
# TODO: Add authentication and rate limiting to this endpoint   

'''
This endpoint allows users to post a chat message to a specific coin's chat.

'''
@router.post("/post-chat")
def post_chat_api(
    request: PostRequest
):

    try:

        result = post_chat(
            coin_url=request.coin_url,
            message=request.message,
            sentiment=request.sentiment
        )

        return result

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }