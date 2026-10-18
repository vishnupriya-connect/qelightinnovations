# QAI.02.03.08 — Boolean filtering lab

This lab practices comparison masks, `&`, `|`, `~`, parentheses, membership filtering, missing-value filtering, label alignment, and nullable Boolean decisions. The mini-project builds a validated learner review queue.

## Run

```bash
python -m pip install -r requirements.txt
python lab.py
python project.py
python -m unittest -v test_project.py
```

`lab.py` should match `expected_lab.txt`. `project.py` should match `expected_project.txt`. The test suite contains 17 tests.

## Files

- `lab.py`: guided examples, controlled variation, and caught failures
- `project.py`: full reference implementation and sample data
- `test_project.py`: correctness, validation, edge-case, and independence tests
- `expected_lab.txt`: exact guided-lab output
- `expected_project.txt`: exact mini-project output
- `requirements.txt`: supported Pandas range

## Evidence checklist

- explain why Pandas masks use `&`, `|`, and `~` rather than scalar Boolean words;
- predict the retained labels for each mask;
- show why parentheses are required;
- explain membership, missing, and non-missing filters;
- demonstrate that a Boolean Series aligns by label;
- state the chosen policy for nullable mask values;
- diagnose the four deliberate failures;
- run all tests and preserve the output.

The examples require no network service, account, API key, or external dataset.
