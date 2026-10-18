"""Guided demonstrations for Pandas label-based row selection."""
import pandas as pd


def sample():
    return pd.DataFrame(
        {
            "learner": ["Anu", "Bala", "Chitra", "Deepa", "Eshan"],
            "python": [72, 85, 91, 68, 88],
            "sql": [80, 77, 89, 75, 90],
        },
        index=["L40", "L10", "L70", "L20", "L60"],
    )


def run():
    df = sample()
    row = df.loc["L10"]
    print("single:", type(row).__name__, row.name, row.shape)
    print("one-row table:", type(df.loc[["L10"]]).__name__, df.loc[["L10"]].shape)
    print("list order:", df.loc[["L20", "L40", "L20"]].index.tolist())
    print("inclusive label slice:", df.loc["L10":"L20"].index.tolist())
    print("reverse label slice:", df.loc["L20":"L10":-1].index.tolist())
    block = df.loc[["L70", "L10"], ["sql", "learner"]]
    print("two-axis block:")
    print(block.to_csv(index=True).strip())
    print("scalar cell:", int(df.loc["L70", "python"]))
    print("one column:", type(df.loc[:, "python"]).__name__, df.loc[:, "python"].shape)
    print("one-column table:", type(df.loc[:, ["python"]]).__name__, df.loc[:, ["python"]].shape)
    for description, operation in [
        ("missing scalar", lambda: df.loc["L99"]),
        ("missing list member", lambda: df.loc[["L10", "L99"]]),
        ("missing column", lambda: df.loc["L10", "Python"]),
    ]:
        try:
            operation()
        except KeyError:
            print(description + ": KeyError")
        else:
            raise AssertionError("Expected KeyError")
    duplicated = pd.DataFrame({"mark": [70, 80, 90]}, index=["A", "A", "B"])
    print("duplicate label result:", type(duplicated.loc["A"]).__name__, duplicated.loc["A"].shape)
    print("variation:")
    print(df.loc[["L60", "L40"], ["learner", "sql"]].to_csv(index=True).strip())


if __name__ == "__main__":
    run()
