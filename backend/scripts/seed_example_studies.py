"""Create example n-of-1 studies with made-up sessions, to explore and edit in the UI.

Every example's title starts with "Example:" and its ratings are invented.

Usage (from backend/):
    PYTHONPATH=. ./venv/bin/python scripts/seed_example_studies.py          # add examples (replaces old ones)
    PYTHONPATH=. ./venv/bin/python scripts/seed_example_studies.py --remove # delete examples only
"""
import argparse
import random
from datetime import date, datetime, time, timedelta

from app.database import SessionLocal
from app.models import Study, StudySession
from app.study_design import block_randomized_schedule

PREFIX = "Example:"

# effect = typical mood (or focus) lift for that condition; completed = sessions already logged
EXAMPLES = [
    {
        "title": f"{PREFIX} Guitar vs Endel vs silence on low mornings",
        "question": "On mornings I wake up low, does playing guitar lift my mood more than listening to Endel or sitting in silence?",
        "conditions": {"Guitar": 2.0, "Endel": 1.2, "Silence": 0.2},
        "minutes": 20,
        "per_condition": 7,
        "completed": 13,
        "measure": "mood",
        "notes": {
            "Guitar": ["Played the new chord progression, lost track of time", "Fingers sore but felt good", "Hard to start, easier after 5 min"],
            "Endel": ["Focus soundscape, felt calmer", "Fell half asleep"],
            "Silence": ["Restless, kept checking phone", "Actually kind of peaceful today"],
        },
    },
    {
        "title": f"{PREFIX} Which tempo helps me focus?",
        "question": "When I'm working, which lo-fi tempo helps me focus best: 70, 90 or 120 BPM?",
        "conditions": {"Lo-fi 70 BPM": 1.0, "Lo-fi 90 BPM": 2.2, "Lo-fi 120 BPM": 0.6},
        "minutes": 45,
        "per_condition": 6,
        "completed": 10,
        "measure": "focus",
        "notes": {
            "Lo-fi 90 BPM": ["Best deep-work block this week"],
            "Lo-fi 120 BPM": ["A bit too energetic, jittery"],
        },
    },
    {
        "title": f"{PREFIX} Singing vs hand drum before bed",
        "question": "Does singing or playing a hand drum for 15 minutes before bed leave me in a better mood?",
        "conditions": {"Singing": 1.6, "Hand drum": 1.1},
        "minutes": 15,
        "per_condition": 5,
        "completed": 4,
        "measure": "mood",
        "notes": {"Singing": ["Sang along to old favourites"]},
    },
]


def clamp(v: float) -> int:
    return max(1, min(10, round(v)))


def remove_examples(db) -> int:
    examples = db.query(Study).filter(Study.title.startswith(PREFIX)).all()
    for study in examples:
        db.delete(study)
    db.commit()
    return len(examples)


def add_examples(db) -> None:
    rng = random.Random(42)
    for spec in EXAMPLES:
        conditions = list(spec["conditions"])
        total = len(conditions) * spec["per_condition"]
        start = date.today() - timedelta(days=spec["completed"])
        study = Study(
            title=spec["title"],
            question=spec["question"],
            conditions=conditions,
            session_minutes=spec["minutes"],
            created_at=datetime.combine(start, time(9)),
        )
        for planned in block_randomized_schedule(conditions, spec["per_condition"], start, rng):
            session = StudySession(**planned)
            if planned["session_number"] <= spec["completed"]:
                effect = spec["conditions"][session.condition]
                mood_before = rng.gauss(4.6, 1.0)
                focus_before = rng.gauss(4.8, 1.0)
                mood_gain = effect if spec["measure"] == "mood" else effect * 0.4
                focus_gain = effect if spec["measure"] == "focus" else effect * 0.5
                session.mood_before = clamp(mood_before)
                session.mood_after = clamp(mood_before + mood_gain + rng.gauss(0, 0.9))
                session.focus_before = clamp(focus_before)
                session.focus_after = clamp(focus_before + focus_gain + rng.gauss(0, 0.9))
                notes = spec["notes"].get(session.condition, [])
                if notes and rng.random() < 0.45:
                    session.notes = rng.choice(notes)
                session.completed_at = datetime.combine(planned["planned_date"], time(8 + rng.randint(0, 11), rng.randint(0, 59)))
            study.sessions.append(session)
        db.add(study)
        print(f"Added {spec['title']!r}: {spec['completed']} of {total} sessions logged")
    db.commit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--remove", action="store_true", help="only delete existing examples")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        removed = remove_examples(db)
        if removed:
            print(f"Removed {removed} existing example studies")
        if not args.remove:
            add_examples(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
