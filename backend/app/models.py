from datetime import datetime, timezone

from sqlalchemy import JSON, Column, Date, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True)
    study_id = Column(String(50), unique=True, nullable=False)
    title = Column(String(500), nullable=False)
    authors = Column(Text)
    abstract = Column(Text)
    year = Column(Integer)
    intervention_type = Column(String(100))  # e.g., "music_alone", "music_pt", "music_ot"
    intervention_details = Column(Text)  # JSON string: {"tempo": 120, "key": "major", "rhythm": "4/4"}
    outcomes = Column(Text)  # JSON: {"outcome_type": "gait", "measure": "cadence", "effect_size": 0.5}
    sample_size = Column(Integer)
    effect_size = Column(Float)
    source = Column(String(50), nullable=False)  # "pubmed", "clinicaltrials"
    url = Column(String(500))
    date_added = Column(DateTime, nullable=False, default=_utcnow)
    created_at = Column(DateTime, nullable=False, default=_utcnow)

    __table_args__ = (
        Index("ix_evidence_source_year", "source", "year"),
        Index("ix_evidence_intervention", "intervention_type"),
    )

    @classmethod
    def from_dict(cls, data: dict) -> "Evidence":
        return cls(**{k: v for k, v in data.items() if k in cls.__table__.columns.keys()})


class Study(Base):
    """A personal n-of-1 study: one person compares conditions across randomized sessions."""

    __tablename__ = "studies"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    question = Column(Text)
    conditions = Column(JSON, nullable=False)  # e.g. ["Guitar", "Endel", "Silence"]
    session_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=_utcnow)

    sessions = relationship(
        "StudySession",
        back_populates="study",
        cascade="all, delete-orphan",
        order_by="StudySession.session_number",
    )


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey("studies.id", ondelete="CASCADE"), nullable=False, index=True)
    session_number = Column(Integer, nullable=False)
    condition = Column(String(100), nullable=False)
    planned_date = Column(Date, nullable=False)
    completed_at = Column(DateTime)
    mood_before = Column(Integer)  # 1-10
    mood_after = Column(Integer)
    focus_before = Column(Integer)
    focus_after = Column(Integer)
    notes = Column(Text)

    study = relationship("Study", back_populates="sessions")
