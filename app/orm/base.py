import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool


class DatabaseConfig:
    @staticmethod
    def get_dsn() -> str:
        db_driver = os.getenv('DB_DRIVER', 'postgresql')

        # Специальная обработка для SQLite
        if db_driver == 'sqlite':
            db_name = os.getenv('DB_NAME', ':memory:')
            return f"sqlite:///{db_name}"

        # Для других БД
        db_user = os.getenv('DB_USER', 'postgres')
        db_pass = os.getenv('DB_PASSWORD', '')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'app_db')

        return f"{db_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


class Database:
    def __init__(self):
        dsn = DatabaseConfig.get_dsn()

        # Специальные параметры для SQLite
        if dsn.startswith('sqlite'):
            self.engine = create_engine(
                dsn,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool
            )
        else:
            self.engine = create_engine(
                dsn,
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

    @property
    def session(self):
        """Альтернативный способ доступа к текущей сессии"""
        return self.ScopedSession

    def create_all(self):
        """Создание всех таблиц"""
        self.Base.metadata.create_all(bind=self.engine)


# Инициализация ORM
db = Database()
Base = db.Base