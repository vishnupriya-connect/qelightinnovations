"""Independent reference: inspect attendance without guessing missing values."""

import pandas as pd


def make_workshops():
    return pd.DataFrame(
        {
            "workshop": ["Python", "SQL", "Pandas", "Charts"],
            "attendees": [12, None, 18, 10],
        },
        index=["W1", "W2", "W3", "W4"],
    )


def main():
    workshops = make_workshops()
    print("shape", workshops.shape)
    print("first", workshops.head(1).index.tolist())
    print("last", workshops.tail(1).index.tolist())
    print("non-null", workshops.count().to_dict())
    print("known mean", round(workshops.describe().loc["mean", "attendees"], 6))
    print("sample labels", workshops.sample(n=2, random_state=42).index.tolist())
    print("estimated bytes", int(workshops.memory_usage(deep=True).sum()))


if __name__ == "__main__":
    main()
