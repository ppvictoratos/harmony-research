import random
from datetime import date, timedelta
from statistics import mean
from typing import Dict, List, Optional


def block_randomized_schedule(
    conditions: List[str],
    sessions_per_condition: int,
    start: date,
    rng: Optional[random.Random] = None,
) -> List[Dict]:
    """One session per day. Each block runs every condition once in shuffled order,
    so conditions stay balanced over time and no condition clusters on good or bad weeks."""
    rng = rng or random.Random()
    schedule = []
    for _ in range(sessions_per_condition):
        block = list(conditions)
        rng.shuffle(block)
        for condition in block:
            schedule.append({
                "session_number": len(schedule) + 1,
                "condition": condition,
                "planned_date": start + timedelta(days=len(schedule)),
            })
    return schedule


def _avg(values: List[float]) -> Optional[float]:
    return round(mean(values), 2) if values else None


def summarize(conditions: List[str], sessions) -> List[Dict]:
    """Per-condition averages over completed sessions. A change is after minus before."""
    summary = []
    for condition in conditions:
        done = [s for s in sessions if s.condition == condition and s.completed_at]
        mood_changes = [s.mood_after - s.mood_before for s in done
                        if s.mood_before is not None and s.mood_after is not None]
        focus_changes = [s.focus_after - s.focus_before for s in done
                         if s.focus_before is not None and s.focus_after is not None]
        summary.append({
            "condition": condition,
            "planned": sum(1 for s in sessions if s.condition == condition),
            "completed": len(done),
            "mood_before_avg": _avg([s.mood_before for s in done if s.mood_before is not None]),
            "mood_after_avg": _avg([s.mood_after for s in done if s.mood_after is not None]),
            "mood_change_avg": _avg(mood_changes),
            "mood_changes": mood_changes,
            "focus_change_avg": _avg(focus_changes),
            "focus_changes": focus_changes,
        })
    return summary
