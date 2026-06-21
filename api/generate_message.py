from fastapi import APIRouter
from pydantic import BaseModel

from modules.message_generator import generate_message

router = APIRouter()


class GenerateMessageRequest(BaseModel):
    # Accept either a full coin object or a minimal {"url": "..."}.
    # The generator currently uses coin fields directly.
    coin: dict


@router.post("/generate-message")
def generate_message_api(payload: GenerateMessageRequest):
    try:
        message = generate_message(payload.coin)
        return {"status": "success", "message": message}
    except Exception as e:
        return {"status": "error", "message": str(e)}

