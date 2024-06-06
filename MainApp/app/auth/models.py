from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated, Optional

from model.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
idcomp = Annotated[Optional[int], mapped_column(ForeignKey('company.id', ondelete="CASCADE"), nullable=True)]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    name: Mapped[str]
    login: Mapped[str] = mapped_column(
        String(length=320), unique=True, nullable=False
    )
    isOwner: Mapped[bool]
    idCompany: Mapped[idcomp]
    email: Mapped[str] = mapped_column(
        nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
