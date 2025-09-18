from pydantic import BaseModel


class Location(BaseModel):
    ip: str
    city: str
    state: str
    lang: str
    longitude: float
    latitude: float
