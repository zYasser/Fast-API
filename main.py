from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, Field
from random import randrange
from faker import Faker
from pprint import pprint

fake = Faker()
print(fake)
app = FastAPI()


class Post(BaseModel):
    title: str = Field(min_length=3)
    content: str
    published: bool = True
    rating: Optional[int] = Field(le=10, ge=0, default=None)


myposts = [
    {
        "id": 1,
        "title": fake.name(),
        "content": fake.text(),
        "rating": randrange(0, 10),
        "published": True,
    },
    {
        "id": 2,
        "title": fake.name(),
        "content": fake.text(),
        "rating": randrange(0, 10),
        "published": True,
    },
]
pprint(myposts)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/all-post")
def getAllPost():
    return myposts


@app.post("/create-post")
def create_posts(post: Post):
    new_post = post.dict()
    new_post["id"] = randrange(0, 100000000)
    myposts.append(new_post)
    pprint(myposts)

    return {"data": new_post}
