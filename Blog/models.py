from sqlalchemy import Column, Boolean, DateTime, ForeignKey, String, Integer, Text
from Blog.database import Base


class User(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(40), unique=True, index=True)
    hashed_password = Column(String(200))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    snippet = Column(Text)
    posted_on = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    body = Column(Text)
    
 
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    
    
class post_like(Base):
    __tablename__ = "post_likes"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    

class post_dislike(Base):
    __tablename__ = "post_dislikes"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    

class comment_like(Base):
    __tablename__ = "comment_likes"
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    

class comment_dislike(Base):
    __tablename__ = "comment_dislikes"
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))