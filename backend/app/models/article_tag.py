from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base

class ArticleTag(Base):
    __tablename__ = "article_tags"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"))
