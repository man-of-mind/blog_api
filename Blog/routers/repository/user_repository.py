from Blog import models, schemas
from sqlalchemy.orm import Session
from Blog.hashing import Hash
from fastapi import HTTPException, status


def create(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, hashed_password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user.id)
    return new_user

def show(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user with the id of {}'.format(user_id))
    return user