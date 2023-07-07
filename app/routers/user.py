from .. import models, schemas, utils
from fastapi import Depends, status, HTTPException, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from ..utils import hash

router = APIRouter(prefix="/user", tags=["Users"])


@router.post(
    "",
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


@router.get("/{id}", response_model=schemas.fetch_user_response)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"user with id: {id} doesn't exit")
    return user
