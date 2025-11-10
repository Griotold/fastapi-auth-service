from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.post import PostCreate
from app.schemas.post import PostUpdate
from app.models.post import Post

class PostService:
    def __init__(self, db: Session) -> None:
        self.db = db

    """
    게시글 생성
    """
    def create_post(self, post: PostCreate) -> Post:
        created_post = Post(**post.model_dump())
        
        self.db.add(created_post)
        self.db.commit()
        self.db.refresh(created_post)
        
        return created_post
    
    """
    전체 게시글 목록 조회
    """
    def get_posts(self) -> list[Post]:
        query = (
            select(Post)
            .order_by(Post.created_at.desc())
        )
        posts = self.db.execute(query).scalars().all()
        return posts
    
    """
    특정 게시글 조회
    """
    def get_post(self, post_id: int) -> Post | None:
        query = (
            select(Post)
            .where(Post.id == post_id)
        )
        post = self.db.execute(query).scalar_one_or_none()
        return post
    
    """
    게시글 수정
    """
    def update_post(self, post_id: int, post_update: PostUpdate) -> Post | None:
        query = (
            select(Post)
            .where(Post.id == post_id)
        )
        post = self.db.execute(query).scalar_one_or_none()

        if post is None:
            return None
        
        update_dict = {
            key: value
            for key, value in post_update.model_dump().items()
            if value is not None
        }

        for key, value in update_dict.items():
            setattr(post, key, value)

        self.db.commit()
        self.db.refresh(post)
        return post
    
    def delete_post(self, post_id: int) -> bool:
        query = (
            select(Post)
            .where(Post.id == post_id)        
        )
        post = self.db.execute(query).scalar_one_or_none()

        if post is None:
            return False
        
        self.db.delete(post)
        self.db.commit()
        return True
    
def get_post_service(db: Session = Depends(get_db)):
    return PostService(db)