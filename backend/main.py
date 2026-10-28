from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import SessionLocal, engine, Base
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# --- 1. DEFINE THE DATABASE TABLE ---
class Idea(Base):
    __tablename__ = "ideas"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    url = Column(String, nullable=True)
    tags = Column(String, nullable=True)

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

# --- 4. GET ENDPOINT (SECURED) ---
@app.get("/ideas")
def get_ideas(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
        
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(
            token, 
            os.getenv("SUPABASE_JWT_SECRET"), 
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        user_email = payload.get("email")
        if not user_email:
            raise Exception("No email in token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")
        
    db = SessionLocal()
    ideas = db.query(Idea).filter(Idea.user_id == user_email).all()
    db.close()
    return ideas

# --- 5. POST ENDPOINT (SECURED) ---
@app.post("/ideas")
def create_idea(idea: IdeaCreate, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
        
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(
            token, 
            os.getenv("SUPABASE_JWT_SECRET"), 
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        user_email = payload.get("email")
        if not user_email:
            raise Exception("No email in token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")

    db = SessionLocal()    
    
    text = idea.content.lower()
    generated_tags = []
    if "app" in text or "build" in text: generated_tags.append("side-project")
    if "habit" in text or "health" in text: generated_tags.append("health")
    if "react" in text or "python" in text or "code" in text: generated_tags.append("coding")
    if "read" in text or "article" in text: generated_tags.append("reading")
    if "ai" in text or "startup" in text: generated_tags.append("business")
    if not generated_tags: generated_tags.append("random-thought")
    tags_string = ", ".join(generated_tags[:3])
    
    new_idea = Idea(
        user_id=user_email, 
        content=idea.content, 
        url=idea.url, 
        tags=tags_string
    )
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    db.close()
    return new_idea