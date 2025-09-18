from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    email: str
    password: str
    gender: Optional[str] = Field(default=None)
    phone_no: Optional[int] = Field(default=None)
    address: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)


class AshaWorker(BaseModel):
    emp_id: int
    name: str
    email: str
    password: str
    gender: Optional[str] = Field(default=None)
    phone_no: Optional[int] = Field(default=None)
    address: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)


class Bmo(BaseModel):
    emp_id: int
    name: str
    email: str
    password: str
    gender: Optional[str] = Field(default=None)
    phone_no: Optional[int] = Field(default=None)
    address: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)


class Govt(BaseModel):
    name: str
    email: str
    password: str
    gender: Optional[str] = Field(default=None)
    phone_no: Optional[int] = Field(default=None)
    address: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)


class Login(BaseModel):
    email: str
    password: str


class Signup(BaseModel):
    emp_id: Optional[int] = Field(default=None)
    name: str
    email: str
    password: str
