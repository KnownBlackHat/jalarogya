from pydantic import BaseModel


class Achivement(BaseModel):
    city: str
    work_type: str
    title: str
    description: str
    image: str
