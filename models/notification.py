from typing import Literal

from pydantic import BaseModel


class Notification(BaseModel):
    role: Literal["asha", "resident", "bmo", "govt"]
    message: str
