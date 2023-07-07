from fastapi import Depends, Response, status, HTTPException, APIRouter

from .. import models, schemas, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/sqlAl")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": posts}


@router.get("/all-post")
def getAllPost(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": posts}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}")
def getPostById(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} doesn't exist",
        )
    return {"data": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"There is no post with Id {id}")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)


@router.put("/{id}")
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
