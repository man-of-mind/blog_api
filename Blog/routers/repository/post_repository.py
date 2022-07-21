from Blog import models, schemas
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def get_all(db: Session):
    posts = db.query(models.Post).all()
    return posts


def create(request: schemas.Post, db: Session):
    new_blog_post = models.Post(title=request.title, body=request.body, snippet=request.snippet, posted_on=request.posted_on)
    db.add(new_blog_post)
    db.commit()
    db.refresh(new_blog_post)
    return new_blog_post


def delete(post_id: int, db: Session):
    post = db.query(models.Post).filter(models.Post.id == post_id).delete(synchronize_session=False);
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog with id {} not found".format(post_id))
    post.delete(synchronize_session=False)
    db.commit()
    return {'response': 'Blog post deleted'}


def update(request: schemas.Post, post_id: int, db: Session):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog with id {} not found".format(post_id))
    post.update(request, synchronize_session=False)
    db.commit()
    return {'response': "Sucessfully updated"}


def show(post_id, db: Session):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No blog post with the id of {}'.format(post_id))
    return post