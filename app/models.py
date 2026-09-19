from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DiaryORM(Base):
    """diaries テーブルの定義"""
    
    __tablename__ = "diaries"
    
    diary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    written_on: Mapped[date] = mapped_column(Date, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    
    