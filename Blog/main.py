from fastapi import FastAPI
from Blog import models, database
from Blog.routers import auth, post, user

app = FastAPI();

models.Base.metadata.create_all(bind=database.engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)