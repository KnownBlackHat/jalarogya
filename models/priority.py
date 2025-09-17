from pydantic import BaseModel


class Priority(BaseModel):
    city: str
    count: int
