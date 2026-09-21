import os
from pathlib import Path

TEST_DB = Path(__file__).resolve().parent / ".cybershield_test.db"

os.environ.setdefault("DATABASE_URL", f"sqlite:///{TEST_DB.as_posix()}")
os.environ.setdefault("SECRET_KEY", "test-only-secret-key-not-for-production")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

def pytest_sessionstart(session):
    if TEST_DB.exists():
        TEST_DB.unlink()

    from app.database.database import Base, engine
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)

def pytest_sessionfinish(session, exitstatus):
    from app.database.database import Base, engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    if TEST_DB.exists():
        TEST_DB.unlink()
