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
