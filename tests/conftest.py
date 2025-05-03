import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_session
from app.api.main import app
from app.orm.base import Database, Base
from app.orm.base import db as main_db
import os

# Переопределяем настройки для тестов
os.environ['DB_DRIVER'] = 'sqlite'
os.environ['DB_NAME'] = ':memory:'


@pytest.fixture(scope="module")
def test_db():
    # Создаем тестовую базу данных
    test_db = Database()
    test_db.engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    test_db.session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db.engine
    )
    test_db.ScopedSession = scoped_session(test_db.session_factory)

    # Создаем таблицы
    Base.metadata.create_all(bind=test_db.engine)

    yield test_db

    # Очищаем после тестов
    Base.metadata.drop_all(bind=test_db.engine)
    test_db.ScopedSession.remove()


@pytest.fixture(scope="module")
def client(test_db):
    # Переопределяем подключение к БД в приложении
    app.dependency_overrides[main_db] = lambda: test_db

    with TestClient(app) as test_client:
        yield test_client

    # Восстанавливаем оригинальное подключение
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def session(test_db):
    """Фикстура для работы с сессией в тестах"""
    connection = test_db.engine.connect()
    transaction = connection.begin()
    session = get_session()

    yield session

    # Откатываем изменения после теста
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_user(client, session):
    user_data = {
        "email": "test@example.com",
        "hashed_password": "stringst",
        "phone_number": "+1234567890",
        "age": 25,
        "sex": "male",
        "grade": "middle"
    }
    res = client.post(
        "/api/auth/register",
        json=user_data
    )
    assert res.status_code == 200, f"Ошибка создания пользователя: {res.text}"
    return res.json()


@pytest.fixture(autouse=True)
def cleanup(session):
    """Автоматическая очистка данных после каждого теста"""
    yield
    with session as db_session:
        try:
            # Откатываем все изменения
            db_session.rollback()

            # Очищаем все таблицы
            for table in reversed(Base.metadata.sorted_tables):
                db_session.execute(table.delete())
            db_session.commit()
        except:
            db_session.rollback()
            raise