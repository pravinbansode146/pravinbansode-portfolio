import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(
    title="Pravin Bansode Portfolio API",
    description="JSON endpoints for portfolio profile, projects, skills, experience, and health.",
    version="1.0.0",
)
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://127.0.0.1:8000").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET"], allow_headers=["*"])

PROFILE = {
    "name": "Pravin Dayanand Bansode",
    "role": "Python Developer",
    "location": "Pune, Maharashtra",
    "email": "pravinbansode147@gmail.com",
    "linkedin": "https://linkedin.com/in/pravin-bansode",
    "skills": ["Python", "SQL", "JavaScript", "Django", "Django REST Framework", "Flask", "PostgreSQL", "MySQL", "Pandas", "NumPy", "Power BI"],
    "projects": [
        {"name":"Pics — Imitation Jewellery E-Commerce", "stack":["Django","DRF","PostgreSQL","JavaScript","Render"], "description":"E-commerce catalogue, cart and shop pages with JSON endpoints for filtering, categories and inventory updates."},
        {"name":"LWT — Learn With Tech", "stack":["Django","DRF","PostgreSQL","HTML","CSS","JavaScript"], "description":"Community learning platform with video tutorials, downloadable study materials and career roadmaps."},
        {"name":"VBI — Virtual Bank of India (Demo)", "stack":["Django","PostgreSQL","HTML","CSS","JavaScript"], "description":"Demo banking application with authentication, balance tracking, deposits and transfers."},
    ],
}
def get_engine():
    url = os.getenv("DATABASE_URL")
    if not url:
        return None
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return create_engine(url, pool_pre_ping=True)

@app.get("/")
def root():
    return {"service": "Pravin Bansode Portfolio API", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok", "database_configured": bool(os.getenv("DATABASE_URL"))}

@app.get("/api/profile")
def profile():
    return PROFILE

@app.get("/api/projects")
def projects():
    return {"count": len(PROFILE["projects"]), "results": PROFILE["projects"]}

@app.get("/api/skills")
def skills():
    return {"results": PROFILE["skills"]}

@app.get("/api/db-check")
def db_check():
    engine = get_engine()
    if engine is None:
        return {"database": "not configured", "hint": "Set DATABASE_URL to enable PostgreSQL check."}
    try:
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version()")).scalar()
        return {"database": "connected", "version": version}
    except SQLAlchemyError:
        return {"database": "unavailable"}
