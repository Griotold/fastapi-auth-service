from fastapi import FastAPI
from app.database import Base, engine
from app.models import post

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
    
@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)

# @app.on_event("startup") 대신에 아래 사용하기
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup (서버 시작할 때)
#     Base.metadata.create_all(bind=engine)
#     yield
#     # Shutdown (서버 종료할 때) - 여기에 정리 코드 작성 가능

# app = FastAPI(lifespan=lifespan)