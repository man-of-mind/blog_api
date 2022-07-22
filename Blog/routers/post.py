from fastapi import APIRouter
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from Blog import schemas, models
from sqlalchemy.orm import Session
from Blog.database import get_db
from typing import List
from Blog.routers.oauth2 import get_current_user
from Blog.routers.repository import post_repository


router = APIRouter(
    prefix="/post",
    tags=['Posts']
)



@router.post('/new/', status_code=status.HTTP_201_CREATED)
def new_blog_post(request: schemas.Post, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return post_repository.create(request, db)


@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowPost])
def blog_posts(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return post_repository.get_all(db)


@router.delete('/{post_id}/remove', status_code=status.HTTP_204_NO_CONTENT)
def remove_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return post_repository.delete(post_id, db)
    

@router.put('/{post_id}/update', status_code=status.HTTP_202_ACCEPTED)
def update_blog(post_id: int, request: schemas.Post, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return post_repository.update(request, post_id, db)


@router.get('/{post_id}', response_model=schemas.ShowPost, status_code=status.HTTP_200_OK)
def blog_post(post_id: int,  db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return post_repository.show(post_id, db)