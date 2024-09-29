from fastapi import FastAPI
from database import model
from database.database import engine

app = FastAPI()

@app.get("/")
def hw():
    return "Hello!!!"

model.Base.metadata.create_all(engine)