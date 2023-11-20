from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
# from sqlmodel import Field, SQLModel
from app.database.db_setup import Base


class Fahrzeuge(Base):
    __tablename__ = "fahrzeuge"

    issi = Column(Integer, index=True, primary_key=True, nullable=False)
    funkrufname = Column(String(), index=True, nullable=False)

#class Fahrzeuge(SQLModel, table=True):
#    issi: int = Field(primary_key=True, nullable=False)
#    funkrufname: str = Field(nullable=False)
