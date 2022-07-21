from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from Blog import schemas, models
from sqlalchemy.orm import Session
from Blog.database import get_db
from Blog.routers.repository import user_repository

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post('/new', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    user_repository.create(request, db)

@router.get('/{user_id}', response_model=schemas.ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_repository.show(user_id, db)