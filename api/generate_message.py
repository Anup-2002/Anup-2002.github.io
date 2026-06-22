from fastapi import APIRouter
from pydantic import BaseModel

from modules.message_generator import generate_message

router = APIRouter()
'''
This endpoint allows users to generate a chat message for a specific coin.
'''

class GenerateMessageRequest(BaseModel):
    coin: dict

@router.post("/generate-message")
def generate_message_api(payload: GenerateMessageRequest):
    try:
        message = generate_message(payload.coin)
        return {"status": "success", "message": message}
    except Exception as e:
        return {"status": "error", "message": str(e)}

