import email
from turtle import st
from fastapi import Depends, Response, status, HTTPException, APIRouter
from ..database import engine, get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import database
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=["auth"])


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Make Sure you entered the correct email and password",
        )
    if not utils.verfiy_password(user.password, user_credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Make Sure you entered the correct email and password",
        )

    access_token = oauth2.create_access_token(data={"username": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
