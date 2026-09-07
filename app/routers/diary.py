from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

router = APIRouter()

@router.get("/diaries")
async def get_diaries():
    pass

@router.get("/diaries/{diary_id}")
async def get_diary():
    pass

@router.post("/diaries")
async def create_diaries():
    pass

@router.put("/diaries/{diary_id}")
async def update_diaries():
    pass

@router.delete("/diaries/{diary_id}")
async def delete_diaries():
    pass

