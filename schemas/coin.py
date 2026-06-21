from pydantic import BaseModel


class CoinRequest(BaseModel):
    url: str

