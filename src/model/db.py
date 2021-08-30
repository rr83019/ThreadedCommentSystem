from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from model.base_models import CommentModel, UserModel, PostModel
from contextlib import contextmanager
from typing import ContextManager

DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = ""
DB_NAME = ""

db = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

UserModel.__table__.create(bind=db, checkfirst=True)
PostModel.__table__.create(bind=db, checkfirst=True)
CommentModel.__table__.create(bind=db, checkfirst=True)


@contextmanager
def session_scope() -> ContextManager[Session]:
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()
