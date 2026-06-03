from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

try:
    engine = create_engine(str(settings.DATABASE_URL) , echo=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
except Exception as e:
    print(f"error : {e}")


class Base(DeclarativeBase):
    pass

