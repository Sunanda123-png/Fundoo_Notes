from pydantic import BaseModel


class UserValidator(BaseModel):
    username: str
    firstname: str
    lastname: str
    password: str
    email: str
    phone: int
    location: str


class LoginUser(BaseModel):
    username: str
    password: str
