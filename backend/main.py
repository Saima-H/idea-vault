from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import SessionLocal, engine, Base

# --- 1. DEFINE THE DATABASE TABLE ---
class Idea(Base):
    __tablename__ = "ideas"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False) # NOT NULL
    url = Column(String, nullable=True)

# Create the table
Base.metadata.create_all(bind=engine)


# --- 2. DEFINE THE PYDANTIC SCHEMA ---
class IdeaCreate(BaseModel):
    content: str
    url: str | None = None


# --- 3. CREATE THE API ---
app = FastAPI()

# Endpoint A: GET all ideas
@app.get("/ideas")
def get_ideas():
    db = SessionLocal()
    ideas = db.query(Idea).all()
    db.close()
    return ideas

# Endpoint B: POST a new idea
@app.post("/ideas")
def create_idea(idea: IdeaCreate):
    db = SessionLocal()
    new_idea = Idea(content=idea.content, url=idea.url)
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    db.close()
    return new_idea