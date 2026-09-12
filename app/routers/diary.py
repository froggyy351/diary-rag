from datetime import date

from fastapi import APIRouter, HTTPException
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
async def get_diaries() -> list[Diary]:
    """登録済みの日記を全て返す"""
    return list(diaries.values())

@router.get("/diaries/{diary_id}")
async def get_diary(diary_id: int) -> Diary:
    """指定された1件を返す。無ければ、404"""
    if diary_id not in diaries:
        raise HTTPException(status_code=404, detail=f"diary_id={diary_id} は見つかりません")
    return diaries[diary_id]

@router.post("/diaries")
async def create_diary(payload: DiaryCreate) -> Diary:
    """日記を1件登録し、採番済みの結果を返す。"""
    diary_id = max(diaries, default=0) + 1
    diary = Diary(diary_id=diary_id, **payload.model_dump())
    diaries[diary_id] = diary
    return diary

@router.put("/diaries/{diary_id}")
async def update_diary(diary_id: int, payload: DiaryCreate) -> Diary:
    """指定された1件を丸ごと差し替える。無ければ404"""
    if diary_id not in diaries:
        raise HTTPException(status_code=404, detail=f"diary_id={diary_id} は見つかりません")
    diary = Diary(diary_id=diary_id, **payload.model_dump()) 
    diaries[diary_id] = diary
    return diary

@router.delete("/diaries/{diary_id}", status_code=204)
async def delete_diary(diary_id: int) -> None:
    """指定された1件を削除する。無ければ404"""
    if diary_id not in diaries:
        raise HTTPException(status_code=404, detail=f"diary_id={diary_id}は見つかりません")
    del diaries[diary_id]

