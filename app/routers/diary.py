from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DiaryORM

router = APIRouter()

class DiaryCreate(BaseModel):
    """日記の作成・更新でクライアントから受け取る形。"""

    written_on: date
    body: str

class Diary(DiaryCreate):
    """API が返す形。採番済みの diary_id を持つ。"""

    model_config = ConfigDict(from_attributes=True)
    
    diary_id: int

def get_diary_or_404(
    diary_id: int, db: Session = Depends(get_db)
) -> DiaryORM:
    """指定された1件を取り出す。無ければ404を投げる"""
    row = db.get(DiaryORM, diary_id)
    if row is None:
        raise HTTPException(
            status_code=404, detail=f"diary_id={diary_id}は見つかりません"
        )
    return row

@router.get("/diaries")
async def get_diaries(db: Session = Depends(get_db)) -> list[Diary]:
    """登録済みの日記を全て返す"""
    rows = db.scalars(select(DiaryORM).order_by(DiaryORM.diary_id)).all()
    return [Diary.model_validate(row) for row in rows]

@router.get("/diaries/{diary_id}")
async def get_diary(row: DiaryORM = Depends(get_diary_or_404)) -> Diary:
    """指定された1件を返す。無ければ、404"""
    return Diary.model_validate(row)

@router.post("/diaries", status_code=201)
async def create_diary(
    payload: DiaryCreate, db: Session = Depends(get_db)
    ) -> Diary:
    """日記を1件登録し、採番済みの結果を返す。"""
    row = DiaryORM(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return Diary.model_validate(row)

@router.put("/diaries/{diary_id}")
async def update_diary(
    payload: DiaryCreate,
    row: DiaryORM = Depends(get_diary_or_404),
    db: Session = Depends(get_db)
    ) -> Diary:
    """指定された1件を丸ごと差し替える。無ければ404"""
    for field, value in payload.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return Diary.model_validate(row)

@router.delete("/diaries/{diary_id}", status_code=204)
async def delete_diary(
    row: DiaryORM = Depends(get_diary_or_404),
    db: Session = Depends(get_db)
    ) -> None:
    """指定された1件を削除する。無ければ404"""
    db.delete(row)
    db.commit()

