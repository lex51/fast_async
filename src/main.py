from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup():
    # await database.connect()
    pass


@app.on_event("shutdown")
async def shutdown():
    # await database.disconnect()
    pass


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


# @app.post("/save_mail")
# async def save_mail(
# ):
#     pass
