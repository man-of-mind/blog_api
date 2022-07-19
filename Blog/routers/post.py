from fastapi import APIRouter
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from Blog import schemas, models
from sqlalchemy.orm import Session
from Blog.database import get_db
from typing import List


router = APIRouter()



@router.post('/blog/new/', status_code=status.HTTP_201_CREATED, tags=['Posts'])
def new_blog_post(request: schemas.Post, db: Session = Depends(get_db)):
    new_blog_post = models.Post(title=request.title, body=request.body, snippet=request.snippet, posted_on=request.posted_on)
    db.add(new_blog_post)
    db.commit()
    db.refresh(new_blog_post)
    return new_blog_post


@router.get('/posts/all', status_code=status.HTTP_200_OK, response_model=List[schemas.Post], tags=['Posts'])
def blog_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.delete('/post/{post_id}/remove', status_code=status.HTTP_204_NO_CONTENT, tags=['Posts'])
def remove_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).delete(synchronize_session=False);
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog with id {} not found".format(post_id))
    post.delete(synchronize_session=False)
    db.commit()
    return {'response': 'Blog post deleted'}
    

@router.put('/post/{post_id}/update', status_code=status.HTTP_202_ACCEPTED, tags=['Posts'])
def update_blog(post_id: int, request: schemas.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog with id {} not found".format(post_id))
    post.update(request, synchronize_session=False)
    db.commit()
    return {'response': "Sucessfully updated"}


@router.get('posts/{post_id}', response_model=schemas.ShowPost, status_code=status.HTTP_200_OK, tags=['Posts'])
def blog_post(post_id: int,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No blog post with the id of {}'.format(post_id))
    return post