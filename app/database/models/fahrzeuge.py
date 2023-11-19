from sqlalchemy import Integer, String, Column
from app.database.db_setup import Base

class Fahrzeuge(Base):
    __tablename__ = "fahrzeuge"

    issi = Column(Integer, index=True, primary_key=True, nullable=False)
    funkrufname = Column(String(), index=True, nullable=False)
