from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Backend is working!"}
    
@app.post("/test")
async def test_endpoint(request: Request):
    data = await request.json()
    print("Полученные данные:", data)
    return {"status": "ok", "received": data}