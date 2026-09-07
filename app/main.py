from fastapi import FastAPI
from pydantic import BaseModel
from app.routers import diary

app = FastAPI()
app.include_router(diary.router)

