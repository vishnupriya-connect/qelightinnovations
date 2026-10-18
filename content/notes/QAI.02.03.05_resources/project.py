"""Build an explicit, ordered learner report without mutating the source."""
import pandas as pd
from lab import sample


def build_report(source):
    """Require unique headers, select allowed fields, then rename them."""
    if not source.columns.is_unique:
        raise ValueError('Source column labels must be unique')
    required = ['student', 'python', 'sql']
    missing = [name for name in required if name not in source.columns]
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    report = source[required].copy()
    report = report.rename(columns={
        'student': 'learner', 'python': 'python_mark', 'sql': 'sql_mark'
    }, errors='raise')
    return report


if __name__ == '__main__':
    print(build_report(sample()).to_csv(index=False).strip())
