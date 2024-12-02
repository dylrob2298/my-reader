from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    link = Column(String, unique=True, index=True)
    summary = Column(String, nullable=True)
    image_url = Column(String, nullable=True)  # New field for image URL
    published_at = Column(DateTime, nullable=True)
    is_read = Column(Boolean, default=False)  # New field for read status
    feed_id = Column(Integer, ForeignKey("feeds.id"))

    # Relationships
    feed = relationship("Feed", back_populates="articles")
    boards = relationship("Board", secondary="article_boards", back_populates="articles")
    tags = relationship("Tag", secondary="article_tags", back_populates="articles")
