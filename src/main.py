from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError

# from fastapi.encoders import jsonable_encoder

from src.crud import EmailDAL
from src.db import Base, async_session, engine
from src.models import EmailDB, EmailSchema


class DefaultResponse(JSONResponse):
    def render(self, content: Any) -> bytes:

        return super().render(
            {
                "api_version": "0.1",
                "ok": True if self.status_code in [200, 201] else False,
                "data": content,
            }
        )


app = FastAPI(default_response_class=DefaultResponse)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    error_list = []
    for error in exc.errors():
        field = error.get("loc")[-1]
        error_list.append(
            {
                "field": field,
                "msg_error": f'{error.get("msg")} ({error.get("type")})',
                "field_original": exc.body.get(field),
            }
        )

    return DefaultResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={  # for structures  --  jsonable_encoder()
            "error": [
                f'Field    \
{i["field"]}   with content    \
{i["field_original"]}   \
{i["msg_error"]}'
                for i in error_list
            ]
        },
    )


@app.post(
    "/save_mail",
    # response_model=EmailDB
    status_code=201,
)
async def save_mail(payload: EmailSchema):
    async with async_session() as session:
        async with session.begin():
            email_dal = EmailDAL(session)
            email = await email_dal.save_mail(payload)

            response_obj: EmailDB = {
                "email": payload.email,
                "uuid": payload.get_uuid,
                "id": email.id,
            }
            return response_obj


@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) if needs..
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    # await database.disconnect()
    pass


@app.get("/ping")
async def pong():
    return "pong!"
