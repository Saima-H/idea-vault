from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import SessionLocal, engine, Base

# --- 1. DEFINE THE DATABASE TABLE ---
class Idea(Base):
    __tablename__ = "ideas"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    url = Column(String, nullable=True)
    tags = Column(String, nullable=True) # <-- Added tags column

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

# Endpoint B: POST a new idea (Now with Smart Tags!)
@app.post("/ideas")
def create_idea(idea: IdeaCreate):
    db = SessionLocal()
    
    # --- MOCK NLP LOGIC ---
    text = idea.content.lower()
    generated_tags = []
    
    if "app" in text or "build" in text: generated_tags.append("side-project")
    if "habit" in text or "health" in text: generated_tags.append("health")
    if "react" in text or "python" in text or "code" in text: generated_tags.append("coding")
    if "read" in text or "article" in text: generated_tags.append("reading")
    if "ai" in text or "startup" in text: generated_tags.append("business")
    
    if not generated_tags:
        generated_tags.append("random-thought")
        
    # Convert list to a comma-separated string (e.g., "side-project, coding")
    tags_string = ", ".join(generated_tags[:3])
    
    # Save to database
    new_idea = Idea(content=idea.content, url=idea.url, tags=tags_string)
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    db.close()
    return new_idea