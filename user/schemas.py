from pydantic import BaseModel, Field


class UserValidator(BaseModel):
    username: str
    firstname: str
    lastname: str
    password: str = Field(min_length=8)
    email: str
    phone: int
    location: str


class LoginUser(BaseModel):
    username: str
    password: str


class ForgetPassword(BaseModel):
    username: str
    email: str


class ResetPassword(BaseModel):
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)
