from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped
# from sqlmodel import Field, SQLModel
from app.database.db_setup import Base


class Fahrzeuge(Base):
    __tablename__ = "fahrzeuge"

    issi: Mapped[int] = mapped_column(Integer, index=True, primary_key=True, nullable=False)
    funkrufname: Mapped[str] = mapped_column(String(), index=True, nullable=False)

#class Fahrzeuge(SQLModel, table=True):
#    issi: int = Field(primary_key=True, nullable=False)
#    funkrufname: str = Field(nullable=False)
