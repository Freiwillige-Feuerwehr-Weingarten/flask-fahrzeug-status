from sqlalchemy import Integer, String, Column, TIMESTAMP
from geoalchemy2 import Geometry
from app.database.db_setup import Base


class Einsatz(Base):
    __tablename__ = "deployment"

    id = Column(Integer, index=True, primary_key=True, nullable=False, autoincrement=True)
    external_deployment_id = Column(Integer)
    external_source = Column(String)
    external_source_id = Column(Integer)
    keyword = Column(String, nullable=False)
    announcement = Column(String)

    location = Column(String)
    location_name = Column(String)
    location_info = Column(String)
    # get_location = Column(Geometry(geometry_type='POINT'), srid=4326)
    reporter_name = Column(String)
    repoter_info = Column(String)
    situation = Column(String)

    timestamp_started = Column(TIMESTAMP(timezone=False), nullable=False)

