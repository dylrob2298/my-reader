from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    # Relationships
    articles = relationship("Article", secondary="article_boards", back_populates="boards")
