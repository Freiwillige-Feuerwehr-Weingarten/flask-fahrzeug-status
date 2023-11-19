from sqlalchemy import Integer, String, Column, TIMESTAMP, ForeignKey
from app.database.db_setup import Base
from app.database.models.fahrzeuge import Fahrzeuge

class Fahrzeug_Status(Base):
    __tablename__ = "fahrzeug_status"

    issi = Column(Integer, ForeignKey("fahrzeuge.issi"), nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=False))
    id = Column(Integer, index=True, primary_key=True, nullable=False)
    # TODO: Need to indicate that issi is a foreign key