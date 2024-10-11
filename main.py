from fastapi import FastAPI
from database import model
from database.database import engine
from router import post

app = FastAPI()

app.include_router(post.router)

model.Base.metadata.create_all(engine)