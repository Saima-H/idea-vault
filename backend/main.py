
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# --- 4. THE SMART TAG GENERATOR (Mock NLP) ---
class TagRequest(BaseModel):
    text: str

@app.post("/generate-tags")
def generate_tags(request: TagRequest):
    text = request.text.lower()
    tags = []
    
    # Simple keyword matching logic
    if "app" in text or "build" in text:
        tags.append("side-project")
    if "habit" in text or "health" in text or "workout" in text:
        tags.append("health")
    if "react" in text or "python" in text or "code" in text or "api" in text:
        tags.append("coding")
    if "read" in text or "article" in text or "book" in text:
        tags.append("reading")
    if "ai" in text or "student" in text or "startup" in text:
        tags.append("business")
        
    # If no keywords matched, give a default tag
    if not tags:
        tags.append("random-thought")
        
    # Return the top 3 tags
    return {"original_text": request.text, "generated_tags": tags[:3]}