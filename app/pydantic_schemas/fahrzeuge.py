from pydantic import BaseModel


class Fahrzeuge(BaseModel):
    issi: int
    funkrufname: str

    class Config:
        from_attributes = True
