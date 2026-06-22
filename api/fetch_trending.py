from fastapi import APIRouter
from pydantic import BaseModel
from modules.fetch_trending import (
    fetch_trending_coins
)

router = APIRouter()

'''
This endpoint allows users to fetch trending coins.
working:
    1. Fetch trending coins from CoinMarketCap.
    2. Return the list of trending coins as a JSON response.
    3. Handle any exceptions that may occur during the process and return an error message if needed.
'''

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