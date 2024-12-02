from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base

class ArticleBoard(Base):
    __tablename__ = "article_boards"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"))
