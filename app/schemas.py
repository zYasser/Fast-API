from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class Post(BaseModel):
    title: str = Field(min_length=3)
    content: str
    published: bool = True


class PostResponse(BaseModel):
    title: str = Field(min_length=3)
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3)

    class Config:
        orm_mode = True


class user_create_account_request(User):
    password: str = Field(min_length=4)


class fetch_user_response(User):
    created_at: datetime
    id: str


class login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]
