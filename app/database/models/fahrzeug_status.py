from sqlalchemy import Integer, String, Column, TIMESTAMP
from app.database.db_setup import Base

class Fahrzeug_Status(Base):
    __tablename__ = "fahrzeug_status"

    issi = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=False))
    id = Column(Integer, index=True, primary_key=True, nullable=False)
    # TODO: Need to indicate that issi is a foreign key