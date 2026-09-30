"""Inspect before changing a small table."""

import io

import pandas as pd


def make_sessions():
    return pd.DataFrame(
        {
            "topic": ["Python", "SQL", "Arrays", "Pandas", "Charts", "Review"],
            "minutes": [10, 20, None, 40, 50, 60],
        },
        index=["R1", "R2", "R3", "R4", "R5", "R6"],
    )


def capture_info(table):
    buffer = io.StringIO()
    table.info(buf=buffer, show_counts=True, memory_usage="deep")
    return buffer.getvalue()


def main():
    sessions = make_sessions()
    print("Full table:")
    print(sessions.to_string())
    print("First two:", sessions.head(2).index.tolist())
    print("Last two:", sessions.tail(2).index.tolist())
    print("Sample:", sessions.sample(n=2, random_state=42).index.tolist())
    print("Shape:", sessions.shape)
    print("Columns:", sessions.columns.tolist())
    print("Index:", sessions.index.tolist())
    print("Dtypes:", {column: str(dtype) for column, dtype in sessions.dtypes.items()})
    print("Information:")
    print(capture_info(sessions), end="")
    print("Non-null:", sessions.count().to_dict())
    print("Numeric statistics:")
    print(sessions.describe().to_string())
    print("All-column statistics:")
    print(sessions.describe(include="all").to_string())
    print("Estimated bytes:", int(sessions.memory_usage(deep=True).sum()))
    known = [10, 20, 40, 50, 60]
    print("Manual mean:", sum(known) / len(known))
    changed = sessions.copy()
    changed.loc["R3", "minutes"] = 30
    print("Variant count:", int(changed.count()["minutes"]))
    print("Variant mean:", changed.describe().loc["mean", "minutes"])


if __name__ == "__main__":
    main()
