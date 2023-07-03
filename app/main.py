from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Field
from random import randrange
from faker import Faker
from pprint import pprint
import psycopg2
from psycopg2.extras import RealDictCursor

fake = Faker()
app = FastAPI()

try:
    conn = psycopg2.connect(
        host="localhost",
        database="FastAPI",
        user="postgres",
        password="root",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print(f"connection has been established")

except Exception as err:
    print(f"Connection to the database has failed \nError: {err}")


class Post(BaseModel):
    title: str = Field(min_length=3)
    content: str
    published: bool = True
    rating: Optional[int] = Field(le=10, ge=0, default=None)


# myposts = [
#     {
#         "id": 1,
#         "title": fake.name(),
#         "content": fake.text(),
#         "rating": randrange(0, 10),
#         "published": True,
#     },
#     {
#         "id": 2,
#         "title": fake.name(),
#         "content": fake.text(),
#         "rating": randrange(0, 10),
#         "published": True,
#     },
# ]
# pprint(myposts)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/all-post")
def getAllPost():
    cursor.execute("""SELECT * FROM POSTS""")
    posts = cursor.fetchall()
    return posts


@app.post("/create-post", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts(title,content,published) VALUES (%s, %s , %s) RETURNING *""",
        (post.title, post.title, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/post/{id}")
def getPostById(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} doesn't exist",
        )
    return {"data": post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM POSTS WHERE id=%s * RETURNING *""", (str(id),))
    deletedPost = cursor.fetchone()
    if deletedPost == None:
        raise HTTPException(status_code=404, detail=f"There is no post with Id {id}")
    conn.commit()
    return Response(status_code=204)
