import logging
from typing import Dict, List

from sqlalchemy.orm import Session

from app.models import Evidence
from app.relevance import is_music_relevant

logger = logging.getLogger(__name__)


def ingest_evidence(studies: List[Dict], db: Session) -> int:
    """Ingest a list of studies into the database, skipping duplicates and off-topic records"""
    ids = {s["study_id"] for s in studies if s.get("study_id")}
    seen = {
        row.study_id
        for row in db.query(Evidence.study_id).filter(Evidence.study_id.in_(ids))
    } if ids else set()

    count = 0
    off_topic = 0
    for study in studies:
        study_id = study.get("study_id")
        if not study_id or not study.get("title"):
            logger.warning(f"Skipping study missing id or title: {study_id}")
            continue
        if study_id in seen:
            logger.debug(f"Skipping duplicate: {study_id}")
            continue
        if not is_music_relevant(study):
            off_topic += 1
            logger.debug(f"Skipping off-topic: {study_id} {study['title'][:80]}")
            continue
        db.add(Evidence.from_dict(study))
        seen.add(study_id)
        count += 1

    db.commit()
    logger.info(f"Ingested {count} new evidence records, skipped {off_topic} off-topic")
    return count
