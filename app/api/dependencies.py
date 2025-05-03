from contextlib import contextmanager
from app.orm.base import db


@contextmanager
def get_session():
    session = db.ScopedSession
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
