from pydantic import BaseModel


class Campaign(BaseModel):
    title: str
    description: str
    start_date: str
    end_date: str
    location: str
    banner: str
