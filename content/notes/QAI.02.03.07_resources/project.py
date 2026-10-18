"""Build an identity-based learner report with explicit schema checks."""
from lab import sample


def learner_report(source, learner_ids):
    if not source.index.is_unique:
        raise ValueError("Source row labels must be unique")
    if len(learner_ids) != len(set(learner_ids)):
        raise ValueError("Requested learner labels must be unique")
    required_columns = ["learner", "python", "sql"]
    missing_columns = [name for name in required_columns if name not in source.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    missing_ids = [label for label in learner_ids if label not in source.index]
    if missing_ids:
        raise ValueError(f"Unknown learner labels: {missing_ids}")
    return source.loc[list(learner_ids), required_columns].copy()


if __name__ == "__main__":
    report = learner_report(sample(), ["L70", "L10"])
    print(report.to_csv(index=True).strip())
