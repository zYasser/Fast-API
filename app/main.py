from fastapi import Depends, FastAPI, Response, status, HTTPException
from faker import Faker
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .utils import hash
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

fake = Faker()
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
