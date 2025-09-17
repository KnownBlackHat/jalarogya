from pydantic import BaseModel


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
    name: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class Signup(BaseModel):
    name: str
    email: str
    password: str
