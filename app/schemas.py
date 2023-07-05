from pydantic import BaseModel, Field


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
    email = str
    username = str


class user_create_account_request(User):
    password: str
