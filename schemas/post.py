from pydantic import BaseModel


class PostRequest(BaseModel):
    coin_url: str
    message: str
    sentiment: str = "bullish"

