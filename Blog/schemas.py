from pydantic import BaseModel
from datetime import datetime
from typing import Union

class BlogModel(BaseModel):
    title: str
    snippet: str
    date: datetime
    body: str
    


class PostBase(BaseModel):
    title: str
    snippet: Union[str, None] = None
    body: str
    posted_on: datetime


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool = False

    class Config:
        orm_mode = True
        

class CommentBase(BaseModel):
    body: str
    

class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int
    likes = int = 0
    dislikes = int = 0

    class Config:
        orm_mode = True
    

class Post_likesBase(BaseModel):
    post_id = int
    user_id = int
    

class Post_likesCreate(Post_likesBase):
    pass


class Post_likes(Post_likesBase):
    id: int
    
    class Config:
        orm_mode = True

    
    
class Post_dislikesBase(BaseModel):
    post_id = int
    user_id = int
    

class Post_dislikesCreate(Post_dislikesBase):
    pass


class Post_dislikes(Post_dislikesBase):
    id: int
    
    class Config:
        orm_mode = True

    
    
class Comment_likesBase(BaseModel):
    comment_id = int
    user_id = int
    

class Comment_likesCreate(Comment_likesBase):
    pass


class Comment_likes(Comment_likesBase):
    id: int
    
    class Config:
        orm_mode = True

    

class Comment_dislikesBase(BaseModel):
    comment_id = int
    user_id = int
    

class Comment_dislikesCreate(Comment_dislikesBase):
    pass


class Comment_dislikes(Comment_dislikesBase):
    id: int
    
    class Config:
        orm_mode = True