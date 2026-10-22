"""Decide whether a record is actually about music, rhythm or sound as an intervention.

Searches are broad on purpose, so a paper can match on a passing mention ("participants
listened to music during the scan"). A record counts when:
- a music term is in its title, or
- its title is about cueing and the abstract mentions auditory or rhythmic cues, or
- the abstract/outcomes mention music terms at least twice.
"""
import re
from typing import Dict, List

MUSIC_TERMS = re.compile(
    r"\b("
    r"music\w*|song\w*|sing|singing|sung|singer\w*|choir\w*|choral|chant\w*|melod\w*|harmoni[cz]\w*"
    r"|orchestra\w*|ensemble|band|rhythm\w*|metronom\w*|beat|beats|tempo|bpm"
    r"|auditory cu\w*|acoustic cu\w*|sound cu\w*|auditory stimul\w*|auditory feedback|sonif\w*"
    r"|danc\w*|tango|drum\w*|percussi\w*|piano|guitar|instrumental|lsvt loud|ronnie gardiner"
    r")\b",
    re.IGNORECASE,
)

CUEING_TITLE = re.compile(r"\bcu(e|es|eing|ing)\b", re.IGNORECASE)

MIN_BODY_MENTIONS = 2


def music_terms(text: str) -> List[str]:
    return [m.lower() for m in MUSIC_TERMS.findall(text or "")]


def is_music_relevant(study: Dict) -> bool:
    if music_terms(study.get("title", "")):
        return True
    body_terms = music_terms(f"{study.get('abstract') or ''} {study.get('outcomes') or ''}")
    if CUEING_TITLE.search(study.get("title", "")) and body_terms:
        return True
    return len(body_terms) >= MIN_BODY_MENTIONS
