from fastapi import FastAPI

from app.api.routers import users, auth, interviews, vacancies, tests, questions
from app.orm.base import Base, db

app = FastAPI()
Base.metadata.drop_all(bind=db.engine)
Base.metadata.create_all(bind=db.engine)
app.include_router(auth.router, tags=["auth"], prefix="/api")
app.include_router(users.router, tags=["users"], prefix="/api")
app.include_router(interviews.router, tags=["interviews"], prefix="/api")
app.include_router(vacancies.router, tags=["vacancies"], prefix="/api")
app.include_router(tests.router, tags=["tests"], prefix="/api")
app.include_router(questions.router, tags=["questions"], prefix="/api")
