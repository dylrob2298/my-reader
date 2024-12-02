from datetime import datetime
from pydantic import BaseModel

class FeedCreate(BaseModel):
    url: str
    title: str | None = None

class FeedResponse(BaseModel):
    id: int
    url: str
    title: str | None

    class Config:
        orm_mode = True

class ArticleResponse(BaseModel):
    id: int
    title: str
    link: str
    summary: str | None
    published_at: datetime | None
    image_url: str | None
    is_read: bool

    class Config:
        orm_mode = True

class BoardCreate(BaseModel):
    name: str

class BoardResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class TagCreate(BaseModel):
    name: str

class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
