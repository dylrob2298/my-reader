import feedparser
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from sqlalchemy.orm import Session
from app.models.feed import Feed
from app.models.article import Article
from app.schemas import FeedCreate

def create_feed(db: Session, feed: FeedCreate):
    new_feed = Feed(url=feed.url, title=feed.title)
    db.add(new_feed)
    db.commit()
    db.refresh(new_feed)
    return new_feed

def get_feeds(db: Session):
    return db.query(Feed).all()

def fetch_articles_from_feed(db: Session, feed_id: int):
    feed = db.query(Feed).filter(Feed.id == feed_id).first()
    if not feed:
        return {"status": "error", "message": "Feed not found"}

    parsed_feed = feedparser.parse(feed.url)
    new_articles = 0

    for entry in parsed_feed.entries:
        if db.query(Article).filter(Article.link == entry.link).first():
            continue

        # Extract image URL (optional based on RSS feed structure)
        image_url = None
        if "media_content" in entry and entry.media_content:
            image_url = entry.media_content[0].get("url")

        published_at = None
        if "published" in entry:
            try:
                published_at = parsedate_to_datetime(entry.published)
            except (TypeError, ValueError):
                pass

        article = Article(
            title=entry.title,
            link=entry.link,
            summary=entry.get("summary", ""),
            image_url=image_url,
            published_at=published_at,
            feed_id=feed.id,
        )
        db.add(article)
        new_articles += 1

    db.commit()
    return {"status": "success", "new_articles": new_articles}