from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_
from sqlalchemy.orm import Query as SAQuery
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Evidence
from app.schemas import Evidence as EvidenceSchema
from app.schemas import EvidenceListResponse, StatsResponse

router = APIRouter(prefix="/api", tags=["evidence"])


def _apply_filters(
    query: SAQuery,
    source: Optional[str],
    year_from: Optional[int],
    year_to: Optional[int],
) -> SAQuery:
    if source:
        query = query.filter(Evidence.source == source)
    if year_from is not None:
        query = query.filter(Evidence.year >= year_from)
    if year_to is not None:
        query = query.filter(Evidence.year <= year_to)
    return query


def _paginate(query: SAQuery, page: int, page_size: int) -> EvidenceListResponse:
    total = query.count()
    # Stable order so pages never repeat or skip rows
    rows = (
        query.order_by(Evidence.year.desc().nulls_last(), Evidence.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return EvidenceListResponse(
        total=total,
        page=page,
        page_size=page_size,
        results=[EvidenceSchema.model_validate(r) for r in rows],
    )


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


@router.get("/evidence", response_model=EvidenceListResponse)
def list_evidence(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    source: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
):
    """List all evidence with pagination"""
    query = _apply_filters(db.query(Evidence), source, year_from, year_to)
    return _paginate(query, page, page_size)


@router.get("/evidence/search", response_model=EvidenceListResponse)
def search_evidence(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    source: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
):
    """Search evidence by title, authors, abstract, or outcomes"""
    pattern = f"%{_escape_like(q.strip())}%"
    query = db.query(Evidence).filter(or_(
        Evidence.title.ilike(pattern, escape="\\"),
        Evidence.authors.ilike(pattern, escape="\\"),
        Evidence.abstract.ilike(pattern, escape="\\"),
        Evidence.outcomes.ilike(pattern, escape="\\"),
    ))
    query = _apply_filters(query, source, year_from, year_to)
    return _paginate(query, page, page_size)


@router.get("/evidence/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """Get aggregate statistics about evidence base"""

    def counts(column):
        result: dict = {}
        for key, n in db.query(column, func.count(Evidence.id)).group_by(column).all():
            label = "unknown" if key is None else str(key)
            result[label] = result.get(label, 0) + n  # NULL and literal "unknown" merge
        return result

    return StatsResponse(
        total_studies=db.query(Evidence).count(),
        by_source=counts(Evidence.source),
        by_year=counts(Evidence.year),
        by_intervention=counts(Evidence.intervention_type),
    )
