from sqlalchemy import Integer, String, Column, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db_setup import Base
from app.database.models.fahrzeuge import Fahrzeuge

class Fahrzeug_Status(Base):
    __tablename__ = "fahrzeug_status"

    issi = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=False))
    id = Column(Integer, index=True, primary_key=True, nullable=False)