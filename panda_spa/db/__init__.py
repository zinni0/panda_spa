from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

repo_root = Path(__file__).parent.parent
db_file = repo_root / "panda_spa.db"

DATABASE_URL = f"sqlite:///{db_file.resolve()}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
