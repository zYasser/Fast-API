from fastapi import Depends, FastAPI, Response, status, HTTPException
from faker import Faker
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .utils import hash
from .database import engine, get_db
from sqlalchemy.orm import Session

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


models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sqlAl")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": posts}


@app.get("/all-post")
def getAllPost(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": posts}


@app.post(
    "/create-post",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/post/{id}")
def getPostById(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} doesn't exist",
        )
    return {"data": post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"There is no post with Id {id}")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)


@app.put("/posts/{id}")
def update_post(updated_post: schemas.Post, id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


@app.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
def createUser(
    user: schemas.user_create_account_request, db: Session = Depends(get_db)
):
    user.password = hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.fetch_user_response)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"user with id: {id} doesn't exit")
    return user
