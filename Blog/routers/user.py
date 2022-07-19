from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from Blog import schemas, models
from sqlalchemy.orm import Session
from Blog.hashing import Hash
from Blog.database import get_db


router = APIRouter()

@router.post('/user/new', response_model=schemas.ShowUser, tags=['user'])
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, hashed_password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{user_id}', response_model=schemas.ShowUser, tags=['user'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user with the id of {}'.format(user_id))
    return user