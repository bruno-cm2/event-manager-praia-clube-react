import os
from typing import Annotated
from dotenv import load_dotenv

from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy import DDL, create_engine, event

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in the environment variables.")

class Base(DeclarativeBase):
    pass

event.listen(
    Base.metadata, "before_create",
    DDL("CREATE EXTENSION IF NOT EXISTS btree_gist"),
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]