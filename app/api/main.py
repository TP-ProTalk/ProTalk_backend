from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.orm.base import Base, db

app = FastAPI()

Base.metadata.create_all(bind=db.engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
