import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import DiaryORM # noqa: F401 Base に登録させるための import

TEST_DATABASE_URL = "postgresql+psycopg://diary:diary@localhost:5432/diary_rag_test"

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False)

@pytest.fixture
def db() -> Session:
    """テストごとに、まっさらなテーブルを用意する。"""
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db: Session) -> TestClient:
    """アプリのDB接続先をテスト用に差し替えた。TestClient"""
    
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear