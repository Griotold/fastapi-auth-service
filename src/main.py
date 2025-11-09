from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from app.database import Base, engine, get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from sqlalchemy.orm import Session


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

# 게시글 생성
@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    created_post = Post(**post.model_dump())

    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    return created_post

# 게시글 목록 조회
@app.get("/posts", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    query = (
        select(Post).
        order_by(Post.created_at.desc())
    )
    posts = db.execute(query).scalars().all()

    # posts = db.query(Post).order_by(Post.created_at_desc()).all()
    
    return posts

# 게시글 상세 조회
@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    query = (
        select(Post).
        where(Post.id == post_id)
    )
    post = db.execute(query).scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    return post

# 게시글 수정
@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    query = (
        select(Post).
        where(Post.id == post_id)
    )
    post = db.execute(query).scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    update_dict = {
        key: value
        for key, value in post_update.model_dump().items()
        if value is not None
    }

    for key, value in update_dict.items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post

# 게시글 삭제
@app.delete("/posts/{post_id}", response_model=dict)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    query = (
        select(Post).
        where(Post.id == post_id)
    )

    post = db.execute(query).scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    db.delete(post)
    db.commit() 
    
    return {"message": "게시글이 성공적으로 삭제되었습니다."}  

    

    

