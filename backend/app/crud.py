from sqlalchemy.orm import Session
from app.models.feed import Feed
from app.schemas import FeedCreate

def create_feed(db: Session, feed: FeedCreate):
    new_feed = Feed(url=feed.url, title=feed.title)
    db.add(new_feed)
    db.commit()
    db.refresh(new_feed)
    return new_feed

def get_feeds(db: Session):
    return db.query(Feed).all()
