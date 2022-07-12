from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session

from Blog import schemas, models, database


app = FastAPI();

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal();
    try:
        yield db
    except:
        db.close()


@app.post('/blog/new/', status_code=status.HTTP_201_CREATED)
def blog_post_comments(request: models.Post, db: Session = Depends(get_db)):
    new_blog_post = models.blog(title=request.title, body=request.title, snippet=request.snippet)
    db.add(new_blog_post)
    db.commit()
    db.refresh(new_blog_post)
    return new_blog_post

@app.get('/posts/all', status_code=status.HTTP_200_OK)
def blog_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get('posts/{post_id}', status_code=status.HTTP_200_OK)
def blog_post(post_id: int, response = Response,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Blog.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No blog post with the id of {}'.format(post_id))
    return post