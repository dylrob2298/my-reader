from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String, nullable=True)
