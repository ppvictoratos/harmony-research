from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.orm import declarative_base

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
