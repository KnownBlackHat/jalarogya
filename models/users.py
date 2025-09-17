from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    email: str
    password: str


class AshaWorker(BaseModel):
    emp_id: int
    name: str
    email: str
    password: str


class Bmo(BaseModel):
    emp_id: int
    name: str
    email: str
    password: str


class Govt(BaseModel):
    name: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class Signup(BaseModel):
    emp_id: Optional[int] = Field(default=None)
    name: str
    email: str
    password: str
