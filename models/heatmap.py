from pydantic import BaseModel


class HeatMap(BaseModel):
    city: str
    count: int
    severity: int
