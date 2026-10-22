from datetime import date, datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Study, StudySession
from app.study_design import block_randomized_schedule, summarize

router = APIRouter(prefix="/api/studies", tags=["studies"])

Rating = Optional[int]


class StudyCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    question: Optional[str] = None
    conditions: List[str] = Field(min_length=2, max_length=6)
    session_minutes: int = Field(20, ge=1, le=240)
    sessions_per_condition: int = Field(7, ge=2, le=30)
    start_date: Optional[date] = None

    @field_validator("conditions")
    @classmethod
    def clean_conditions(cls, value: List[str]) -> List[str]:
        cleaned = [c.strip() for c in value]
        if any(not c or len(c) > 100 for c in cleaned):
            raise ValueError("each condition needs a name of 1-100 characters")
        if len({c.lower() for c in cleaned}) != len(cleaned):
            raise ValueError("condition names must be different")
        return cleaned


class SessionUpdate(BaseModel):
    mood_before: Rating = Field(None, ge=1, le=10)
    mood_after: Rating = Field(None, ge=1, le=10)
    focus_before: Rating = Field(None, ge=1, le=10)
    focus_after: Rating = Field(None, ge=1, le=10)
    notes: Optional[str] = None
    completed: Optional[bool] = None


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_number: int
    condition: str
    planned_date: date
    completed_at: Optional[datetime]
    mood_before: Rating
    mood_after: Rating
    focus_before: Rating
    focus_after: Rating
    notes: Optional[str]


class StudySummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    question: Optional[str]
    conditions: List[str]
    session_minutes: int
    created_at: datetime
    total_sessions: int
    completed_sessions: int


class StudyDetail(StudySummary):
    sessions: List[SessionOut]


class ConditionResult(BaseModel):
    condition: str
    planned: int
    completed: int
    mood_before_avg: Optional[float]
    mood_after_avg: Optional[float]
    mood_change_avg: Optional[float]
    mood_changes: List[int]
    focus_change_avg: Optional[float]
    focus_changes: List[int]


class StudyResults(BaseModel):
    study_id: int
    completed_sessions: int
    total_sessions: int
    conditions: List[ConditionResult]


def _summary(study: Study) -> dict:
    return {
        "id": study.id,
        "title": study.title,
        "question": study.question,
        "conditions": study.conditions,
        "session_minutes": study.session_minutes,
        "created_at": study.created_at,
        "total_sessions": len(study.sessions),
        "completed_sessions": sum(1 for s in study.sessions if s.completed_at),
    }


def _get_study(db: Session, study_id: int) -> Study:
    study = db.get(Study, study_id)
    if study is None:
        raise HTTPException(status_code=404, detail="Study not found")
    return study


@router.post("", response_model=StudyDetail, status_code=201)
def create_study(body: StudyCreate, db: Session = Depends(get_db)):
    study = Study(
        title=body.title.strip(),
        question=(body.question or "").strip() or None,
        conditions=body.conditions,
        session_minutes=body.session_minutes,
    )
    start = body.start_date or date.today()
    for planned in block_randomized_schedule(body.conditions, body.sessions_per_condition, start):
        study.sessions.append(StudySession(**planned))
    db.add(study)
    db.commit()
    db.refresh(study)
    return {**_summary(study), "sessions": study.sessions}


@router.get("", response_model=List[StudySummary])
def list_studies(db: Session = Depends(get_db)):
    studies = db.query(Study).order_by(Study.created_at.desc(), Study.id.desc()).all()
    return [_summary(s) for s in studies]


@router.get("/{study_id}", response_model=StudyDetail)
def get_study(study_id: int, db: Session = Depends(get_db)):
    study = _get_study(db, study_id)
    return {**_summary(study), "sessions": study.sessions}


@router.delete("/{study_id}", status_code=204)
def delete_study(study_id: int, db: Session = Depends(get_db)):
    db.delete(_get_study(db, study_id))
    db.commit()


@router.patch("/{study_id}/sessions/{session_id}", response_model=SessionOut)
def update_session(study_id: int, session_id: int, body: SessionUpdate, db: Session = Depends(get_db)):
    session = db.get(StudySession, session_id)
    if session is None or session.study_id != study_id:
        raise HTTPException(status_code=404, detail="Session not found")

    for field in ("mood_before", "mood_after", "focus_before", "focus_after", "notes"):
        if field in body.model_fields_set:
            setattr(session, field, getattr(body, field))

    if body.completed is True:
        if session.mood_before is None or session.mood_after is None:
            raise HTTPException(status_code=422, detail="Rate your mood before and after to complete a session")
        session.completed_at = session.completed_at or datetime.now(timezone.utc).replace(tzinfo=None)
    elif body.completed is False:
        session.completed_at = None

    db.commit()
    db.refresh(session)
    return session


@router.get("/{study_id}/results", response_model=StudyResults)
def get_results(study_id: int, db: Session = Depends(get_db)):
    study = _get_study(db, study_id)
    return {
        "study_id": study.id,
        "completed_sessions": sum(1 for s in study.sessions if s.completed_at),
        "total_sessions": len(study.sessions),
        "conditions": summarize(study.conditions, study.sessions),
    }
