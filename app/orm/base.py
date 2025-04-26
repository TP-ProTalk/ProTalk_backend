import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


class DatabaseConfig:
    @staticmethod
    def get_dsn() -> str:
        db_driver = os.getenv('DB_DRIVER', 'postgresql')
        db_user = os.getenv('DB_USER', 'postgres')
        db_pass = os.getenv('DB_PASSWORD', '')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'app_db')

        return f"{db_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


class Database:
    def __init__(self):
        self.engine = create_engine(
            DatabaseConfig.get_dsn(),
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )
        self.ScopedSession = scoped_session(self.session_factory)
        self.Base = declarative_base()

    def create_all(self):
        self.Base.metadata.create_all(bind=self.engine)


# Инициализация ORM
db = Database()
Base = db.Base