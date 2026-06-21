from fastapi import APIRouter
from pydantic import BaseModel
from modules.fetch_trending import (
    fetch_trending_coins
)

router = APIRouter()

class CoinRequest(BaseModel): 
    url: str
@router.get("/fetch-trending")
def fetch_trending_api():

    try:

        coins = fetch_trending_coins()

        return {
            "status": "success",
            "count": len(coins),
            "coins": coins
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }