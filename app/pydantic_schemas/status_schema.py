from pydantic import BaseModel
from datetime import datetime


class Status(BaseModel):
    issi: int
    status: str
    timestamp: datetime = None
    id: int


    class Config:
        from_attributes = True
