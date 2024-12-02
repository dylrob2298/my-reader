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
