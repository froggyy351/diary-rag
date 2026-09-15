from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "postgresql+psycopg://diary:diary@localhost:5432/diary_rag"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """テーブル定義の"共有の親"""

def get_db() -> Generator[Session]:
    """リクエストごとにDBとの接続を1本用意し、終わったら閉じる"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

