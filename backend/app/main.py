from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.base import Base
# from app.models.feed import Feed
from app.schemas import FeedCreate, FeedResponse
from app.crud import create_feed, get_feeds

# Initialize FastAPI app
app = FastAPI()

# Initialize the database
Base.metadata.create_all(bind=engine)

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route: Add a new RSS feed
@app.post("/feeds/", response_model=FeedResponse)
def add_feed(feed: FeedCreate, db: Session = Depends(get_db)):
    return create_feed(db, feed)

# Route: List all RSS feeds
@app.get("/feeds/", response_model=list[FeedResponse])
def list_feeds(db: Session = Depends(get_db)):
    return get_feeds(db)
