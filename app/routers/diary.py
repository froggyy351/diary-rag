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


# メモリ上の仮の置き場所。W2 で PostgreSQL に置き換える。
diaries: dict[int, Diary] = {}


@router.get("/diaries")
async def get_diaries():
    pass

@router.get("/diaries/{diary_id}")
async def get_diary():
    pass

@router.post("/diaries")
async def create_diary(payload: DiaryCreate) -> Diary:
    """日記を1件登録し、採番済みの結果を返す。"""
    diary_id = max(diaries, default=0) + 1
    diary = Diary(diary_id=diary_id, **payload.model_dump())
    diaries[diary_id] = diary
    return diary

@router.put("/diaries/{diary_id}")
async def update_diaries():
    pass

@router.delete("/diaries/{diary_id}")
async def delete_diaries():
    pass

