from fastapi import FastAPI
from app.routers import diary

app = FastAPI()
app.include_router(diary.router)

