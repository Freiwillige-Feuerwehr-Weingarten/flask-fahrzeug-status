from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db_setup import Base


class Status(Base):
    __tablename__ = "fahrzeug_status"

    issi: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False))
    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True, nullable=False)
