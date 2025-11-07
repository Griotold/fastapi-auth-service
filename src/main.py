from fastapi import FastAPI
from app.database import engine

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

# 데이터베이스 체크!
@app.get("/ping")
async def pind_db():
    try:
        with engine.connect() as conn:
            return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}