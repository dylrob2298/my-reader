from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.base import Base
# from app.models.feed import Feed
from app.models.article import Article
from app.models.board import Board
from app.models.tag import Tag
from app.schemas import FeedCreate, FeedResponse, ArticleResponse, BoardResponse, BoardCreate, TagCreate, TagResponse
from app.crud import create_feed, get_feeds, fetch_articles_from_feed

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

@app.post("/feeds/{feed_id}/fetch_articles/")
def fetch_articles(feed_id: int, db: Session = Depends(get_db)):
    result = fetch_articles_from_feed(db, feed_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": f"Fetched articles for feed {feed_id}", "new_articles": result["new_articles"]}

@app.get("/feeds/{feed_id}/articles/", response_model=list[ArticleResponse])
def get_articles(feed_id: int, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.feed_id == feed_id).all()
    return articles

@app.patch("/articles/{article_id}/read/")
def mark_article_as_read(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.is_read = True
    db.commit()
    return {"message": f"Article {article_id} marked as read"}

@app.patch("/articles/{article_id}/unread/")
def mark_article_as_unread(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.is_read = False
    db.commit()
    return {"message": f"Article {article_id} marked as unread"}

@app.post("/boards/{board_id}/articles/{article_id}/")
def add_article_to_board(board_id: int, article_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    article = db.query(Article).filter(Article.id == article_id).first()
    if not board or not article:
        raise HTTPException(status_code=404, detail="Board or Article not found")
    board.articles.append(article)
    db.commit()
    return {"message": f"Article {article_id} added to Board {board_id}"}

@app.delete("/boards/{board_id}/articles/{article_id}/")
def remove_article_from_board(board_id: int, article_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    article = db.query(Article).filter(Article.id == article_id).first()
    if not board or not article:
        raise HTTPException(status_code=404, detail="Board or Article not found")
    if article in board.articles:
        board.articles.remove(article)
        db.commit()
        return {"message": f"Article {article_id} removed from Board {board_id}"}
    return {"message": f"Article {article_id} was not in Board {board_id}"}

@app.post("/articles/{article_id}/tags/")
def tag_article(article_id: int, tag_name: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.add(tag)

    article.tags.append(tag)
    db.commit()
    return {"message": f"Tag '{tag_name}' added to Article {article_id}"}

@app.delete("/articles/{article_id}/tags/")
def untag_article(article_id: int, tag_name: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag '{tag_name}' not found")
    if tag in article.tags:
        article.tags.remove(tag)
        db.commit()
        return {"message": f"Tag '{tag_name}' removed from Article {article_id}"}
    return {"message": f"Tag '{tag_name}' was not associated with Article {article_id}"}

@app.get("/boards/", response_model=list[BoardResponse])
def get_all_boards(db: Session = Depends(get_db)):
    boards = db.query(Board).all()
    return boards

@app.get("/boards/{board_id}/articles/", response_model=list[ArticleResponse])
def get_articles_for_board(board_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board.articles

@app.post("/boards/", response_model=BoardResponse)
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    # Check if the board already exists
    existing_board = db.query(Board).filter(Board.name == board.name).first()
    if existing_board:
        raise HTTPException(status_code=400, detail="Board already exists")

    # Create and save the new board
    new_board = Board(name=board.name)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

@app.post("/tags/", response_model=TagResponse)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    # Check if the tag already exists
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")

    # Create and save the new tag
    new_tag = Tag(name=tag.name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

@app.get("/tags/", response_model=list[TagResponse])
def get_all_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return tags