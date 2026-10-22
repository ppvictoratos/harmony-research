from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class EvidenceBase(BaseModel):
    title: str
    authors: Optional[str] = None
    year: Optional[int] = None
    abstract: Optional[str] = None
    intervention_type: Optional[str] = None
    outcomes: Optional[str] = None
    sample_size: Optional[int] = None
    effect_size: Optional[float] = None
    source: str
    url: Optional[str] = None


class EvidenceCreate(EvidenceBase):
    study_id: str


class Evidence(EvidenceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    study_id: str
    date_added: datetime


class EvidenceListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: List[Evidence]


class StatsResponse(BaseModel):
    total_studies: int
    by_source: Dict[str, int]
    by_year: Dict[str, int]  # "unknown" for missing years
    by_intervention: Dict[str, int]  # "unknown" for missing types
