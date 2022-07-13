from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
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
def new_blog_post(request: models.Post, db: Session = Depends(get_db)):
    new_blog_post = models.Post(title=request.title, body=request.title, snippet=request.snippet)
    db.add(new_blog_post)
    db.commit()
    db.refresh(new_blog_post)
    return new_blog_post


@app.get('/posts/all', status_code=status.HTTP_200_OK, response_model=[schemas.PostCreate])
def blog_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.delete('/post/{post_id}/remove', status_code=status.HTTP_204_NO_CONTENT)
def remove_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).delete(synchronize_session=False);
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog with id {} not found".format(post_id))
    post.delete(synchronize_session=False)
    db.commit()
    return {'response': 'Blog post deleted'}
    

@app.put('/post/{post_id}/update', status=status.HTTP_202_ACCEPTED)
def update_blog(post_id: int, request: models.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog with id {} not found".format(post_id))
    post.update(request, synchronize_session=False)
    db.commit()
    return {'response': "Sucessfully updated"}


@app.get('posts/{post_id}', status_code=status.HTTP_200_OK)
def blog_post(post_id: int, response = Response,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Blog.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No blog post with the id of {}'.format(post_id))
    return post


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/user/new', response_model=schemas.User)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user