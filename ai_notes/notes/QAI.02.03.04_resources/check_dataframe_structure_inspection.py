"""Verify previews, statistics, a controlled variant, and failures."""

import math

import pandas as pd

from dataframe_structure_inspection import capture_info, make_sessions
from mini_project_reference import make_workshops


def main():
    sessions = make_sessions()
    assert sessions.shape == (6, 2)
    assert sessions.columns.tolist() == ["topic", "minutes"]
    assert sessions.index.tolist() == ["R1", "R2", "R3", "R4", "R5", "R6"]
    assert sessions.head(1).index.tolist() == ["R1"]
    assert sessions.tail(1).index.tolist() == ["R6"]
    assert len(sessions.head()) == 5
    assert len(sessions.tail()) == 5
    assert isinstance(sessions.head(1), pd.DataFrame)
    sample = sessions.sample(n=2, random_state=42)
    assert sample.equals(sessions.sample(n=2, random_state=42))
    assert len(sample) == 2 and sample.index.is_unique
    assert set(sample.index).issubset(sessions.index)
    assert sessions.count().to_dict() == {"topic": 6, "minutes": 5}
    assert pd.api.types.is_float_dtype(sessions["minutes"].dtype)
    summary = sessions.describe()
    assert summary.columns.tolist() == ["minutes"]
    assert summary.loc["count", "minutes"] == 5
    assert summary.loc["mean", "minutes"] == 36
    assert summary.loc["min", "minutes"] == 10
    assert summary.loc["max", "minutes"] == 60
    assert summary.loc["50%", "minutes"] == 40
    assert sessions.describe(include="all").loc["unique", "topic"] == 6
    info = capture_info(sessions)
    assert "Non-Null Count" in info and "memory usage:" in info
    assert int(sessions.memory_usage(deep=True).sum()) > 0
    changed = sessions.copy()
    changed.loc["R3", "minutes"] = 30
    assert changed.count()["minutes"] == 6
    assert changed.describe().loc["mean", "minutes"] == 35
    assert pd.isna(sessions.loc["R3", "minutes"])
    try:
        sessions.shape()
    except TypeError:
        pass
    else:
        raise AssertionError("Calling shape as a method must fail.")
    try:
        sessions.sample(n=7, random_state=42)
    except ValueError:
        pass
    else:
        raise AssertionError("Cannot sample seven distinct rows from six.")
    workshops = make_workshops()
    assert workshops.shape == (4, 2)
    assert workshops.count().to_dict() == {"workshop": 4, "attendees": 3}
    assert math.isclose(workshops.describe().loc["mean", "attendees"], 40 / 3)
    print("All checks passed.")


if __name__ == "__main__":
    main()
