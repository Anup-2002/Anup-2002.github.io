from fastapi import FastAPI

from api.check_login import (
    router as check_login_router
)

from api.fetch_trending import (
    router as fetch_trending_router
)

from api.generate_message import (
    router as generate_message_router
)

from api.post_chat import (
    router as post_chat_router
)

from api.full_flow import (
    router as full_flow_router
)


app = FastAPI(

    title="CoinMarketCap Bot",

    description="Automated CoinMarketCap Chat Bot",

    version="1.0.0"
)


app.include_router(

    check_login_router,

    tags=["Login"]

)


app.include_router(

    fetch_trending_router,

    tags=["Trending Coins"]

)


app.include_router(

    generate_message_router,

    tags=["Message Generation"]

)


app.include_router(

    post_chat_router,

    tags=["Chat Posting"]

)


app.include_router(

    full_flow_router,

    tags=["Full Flow"]

)


@app.get("/")
def root():

    return {

        "status": "success",

        "message": "CoinMarketCap Bot Running"

    }