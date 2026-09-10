from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class DiaryCreate(BaseModel):
    """日記の作成・更新でクライアントから受け取る形。"""

    written_on: date
    body: str


class Diary(DiaryCreate):
    """API が返す形。採番済みの diary_id を持つ。"""

    diary_id: int

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

