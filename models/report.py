from pydantic import BaseModel


class Report(BaseModel):
    city: str
    state: str
    description: str
    language: str
    image_url: str
    full_address: str
