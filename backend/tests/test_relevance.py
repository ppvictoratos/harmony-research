import pytest

from app.relevance import is_music_relevant


@pytest.mark.parametrize("study", [
    {"title": "Music therapy for Parkinson's disease"},
    {"title": "PARKinSOUND 2.0: participation in an orchestra"},
    {"title": "Effects of the Ronnie Gardiner Method on cognition"},
    {"title": "Gait training", "abstract": "Walking to a metronome and to music."},
    {"title": "One cue does not fit all", "abstract": "Auditory cues improved gait."},
    {"title": "Trial", "outcomes": "Singing voice loudness|Melodic intonation"},
])
def test_relevant(study):
    assert is_music_relevant(study)


@pytest.mark.parametrize("study", [
    {"title": "Deep Brain Stimulation Microelectrodes as a Source of RNA", "abstract": "During a music task."},
    {"title": "Pilates for balance", "abstract": "No sound involved."},
    {"title": "Tactile cueing for freezing of gait", "abstract": "Vibration on the wrist."},
    {"title": "Instrumented gait analysis", "abstract": ""},
])
def test_not_relevant(study):
    assert not is_music_relevant(study)
