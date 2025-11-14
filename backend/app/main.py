from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, select
from sqlalchemy.exc import SQLAlchemyError
from app.db import engine, get_session
from app.models import Survey
import os

app = FastAPI(title="Student Survey API")

# --- Allow frontend (React/Vite) to connect ---
#origins = ["http://localhost:5173"]
origins_env = os.getenv("CORS_ORIGINS", "")
origins = [o.strip() for o in origins_env.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Create tables automatically on startup ---
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# --- Health Check Endpoint ---
@app.get("/health")
def health():
    return {"status": "ok"}

# --- Create Survey (POST) ---
@app.post("/surveys", response_model=Survey)
def create_survey(survey: Survey, session=Depends(get_session)):
    try:
        session.add(survey)
        session.commit()
        session.refresh(survey)
        return survey
    except SQLAlchemyError as e:
        session.rollback()
        print("❌ Database Error:", str(e))  # <-- add this line
        raise HTTPException(status_code=400, detail=str(e))

# --- List all Surveys (GET) ---
@app.get("/surveys", response_model=list[Survey])
def read_surveys(session=Depends(get_session)):
    surveys = session.exec(select(Survey)).all()
    return surveys

# --- Delete Survey (DELETE) ---
@app.delete("/surveys/{survey_id}")
def delete_survey(survey_id: int, session=Depends(get_session)):
    survey = session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    session.delete(survey)
    session.commit()
    return {"deleted_id": survey_id}

@app.put("/surveys/{survey_id}")
def update_survey(survey_id: int, updated_data: dict, session=Depends(get_session)):
    survey = session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    for key, value in updated_data.items():
        if hasattr(survey, key):
            setattr(survey, key, value)
    
    session.add(survey)
    session.commit()
    session.refresh(survey)
    return survey

@app.get("/surveys/{survey_id}", response_model=Survey)
def get_survey(survey_id: int, session=Depends(get_session)):
    survey = session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey
