from sqlalchemy import Integer, String, Column, TIMESTAMP, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from datetime import datetime
from typing import List
from app.database.db_setup import Base


class Einsatz(Base):
    __tablename__ = "deployment"
    
    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True, nullable=False, autoincrement=True)
    external_deployment_id: Mapped[int] = mapped_column(Integer)
    external_source: Mapped[str] = mapped_column(String)
    external_source_id: Mapped[int] = mapped_column(Integer)
    keyword: Mapped[str] = mapped_column(String, nullable=False)
    announcement: Mapped[str] = mapped_column(String)

    location: Mapped[str] = mapped_column(String)
    location_name: Mapped[str] = mapped_column(String)
    location_info: Mapped[str] = mapped_column(String)
    # geo_location = mapped_column(Geometry(geometry_type='POINT'), srid=4326)
    reporter_name: Mapped[str] = mapped_column(String)
    repoter_info: Mapped[str] = mapped_column(String)
    situation: Mapped[str] = mapped_column(String)

    timestamp_started: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=False)
    children: Mapped[List["Einheiten"]] = relationship()


class Einheiten(Base):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True, nullable=False)
    deployment_id: Mapped[int] = mapped_column(ForeignKey("deployment.id"))