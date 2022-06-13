from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import func

# import uuid
from sqlalchemy.dialects.postgresql import UUID

from src.db import Base

from pydantic import BaseModel, EmailStr, UUID4

# SQLAlchemy
class EmailStore(Base):
    __tablename__ = "Emails"
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    uuid = Column(UUID(as_uuid=True))
    # uuid = Column(String)#type, default=uuid4)
    email = Column(String)


from pydantic import Field


class EmailSchema(BaseModel):

    email: EmailStr
    uuid: UUID4 = Field(example="5b80f47c-951b-4979-9c81-1fa5544d63d5")

    @property
    def get_uuid(self):
        return self.uuid.__str__()


class EmailDB(EmailSchema):
    id: int
