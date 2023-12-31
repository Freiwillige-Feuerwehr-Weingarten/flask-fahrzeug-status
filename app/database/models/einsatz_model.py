from datetime import datetime
from typing import List
# from geoalchemy2 import Geometry

from sqlalchemy import Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db_setup import Base


class Einsatz(Base):
    __tablename__ = "deployment"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True, nullable=False, autoincrement=True)
    external_deployment_id: Mapped[int] = mapped_column(Integer, nullable=True)
    external_source: Mapped[str] = mapped_column(String, nullable=True)
    external_source_id: Mapped[int] = mapped_column(Integer, nullable=True)
    keyword: Mapped[str] = mapped_column(String, nullable=False)
    keyword_lst: Mapped[str] = mapped_column(String, nullable=True)
    announcement: Mapped[str] = mapped_column(String, nullable=True)

    location: Mapped[str] = mapped_column(String, nullable=True)
    location_name: Mapped[str] = mapped_column(String, nullable=True)
    location_info: Mapped[str] = mapped_column(String, nullable=True)
    location_longitude: Mapped[float] = mapped_column(Float, nullable=True)
    location_latitude: Mapped[float] = mapped_column(Float, nullable=True)
    # geo_location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    reporter_name: Mapped[str] = mapped_column(String, nullable=True) # should move to additonal info
    reporter_info: Mapped[str] = mapped_column(String, nullable=True) # should move to additional info
    situation: Mapped[str] = mapped_column(String, nullable=True)

    timestamp_started: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=False)
    children: Mapped[List["Einheiten"]] = relationship()


class Einheiten(Base):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    deployment_id: Mapped[int] = mapped_column(ForeignKey("deployment.id"))
