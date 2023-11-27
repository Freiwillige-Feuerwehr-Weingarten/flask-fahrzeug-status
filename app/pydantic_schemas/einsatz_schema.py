from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from geojson_pydantic.geometries import Point

class Einsatz(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_deployment_id: Optional[int] = None
    external_source: Optional[str] = None
    external_source_id: Optional[int] = None
    keyword: str
    keyword_lst: str
    announcement: Optional[str] = None

    location: Optional[str] = None
    location_name: Optional[str] = None
    location_info: Optional[str] = None
    # geo_location = Column(Geography(geometry_type='POINT'), srid=4326)
    geo_location: Optional[Point] = None
    reporter_name: Optional[str] = None
    repoter_info: Optional[str] = None
    situation: Optional[str] = None

    timestamp_started: datetime = None
    # TODO: If not set make sure that a timestamp is used when this was commited against the API
    class Config:
        from_attributes = True


class Einheit(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    unit: str
    deployment_id: Optional[int] = Field(default=None)
    external_source: Optional[str] = Field(default=None)
    external_deployment_id: Optional[int] = Field(default=None)
    class Config:
        from_attributes = True