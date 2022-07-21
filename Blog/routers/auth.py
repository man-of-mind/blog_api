from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from Blog import schemas, models
from Blog.database import get_db
from sqlalchemy.orm import Session
from Blog.hashing import Hash
from Blog.routers.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request: schemas.Login, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return user