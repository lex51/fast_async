from sqlalchemy.orm import Session

from src.models import EmailStore, EmailSchema, EmailDB


class EmailDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def save_mail(self, payload: EmailSchema) -> EmailDB:
        new_email = EmailStore(email=payload.email, uuid=payload.uuid)
        self.db_session.add(new_email)
        await self.db_session.flush()
        return new_email
