from fastapi import FastAPI
from database import model
from database.database import engine
from router import post, user
from auth import authentication
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(post.router)

model.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')