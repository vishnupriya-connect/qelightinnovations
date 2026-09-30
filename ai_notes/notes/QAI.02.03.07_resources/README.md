# Row selection by label lab

This local lab demonstrates label-based row identity with `loc`, including scalar and list requests, inclusive label slices, reverse slices, two-axis selection, missing labels, and duplicate-index behavior. The learner data is invented. No account, external dataset, API key, or paid service is required.

## Run

Use Python 3.11 or later and Pandas 2.2 or 3.x:

```bash
python -m pip install -r requirements.txt
python lab.py
python project.py
python -m unittest -v test_project.py
```

`lab.py` is the guided demonstration. `project.py` contains the full mini-project reference. `test_project.py` contains 15 behavioral tests. `expected_lab.txt` and `expected_project.txt` contain exact standard output.

## Independent project

Implement `learner_report(source, learner_ids)` before inspecting the reference. Require a unique source index, unique request labels, and the fields `learner`, `python`, and `sql`. Report all unknown labels, preserve request order, and return an independent table. An empty request against a valid source must produce shape `(0, 3)`.

The reference validates schema and identity-selection assumptions. It does not validate mark ranges, missing cell values, or whether the source assigned the correct ID to each person.

## Expected project result

The request `['L70', 'L10']` prints:

```text
,learner,python,sql
L70,Chitra,91,89
L10,Bala,85,77
```

## Debug record

- `L99` is absent: scalar and list-based requests raise `KeyError`.
- `Python` is not the column label `python`: column lookup is case-sensitive.
- `loc['L10':'L20']` includes both boundary labels and the intervening `L70` row in current order.
- A duplicate index label can make scalar lookup return multiple rows. The project rejects a non-unique source index.
- A repeated requested ID repeats a row in ordinary `loc` selection. The project rejects it because this report requires each learner once.

## Evidence

Save passing test output, compare both scripts with their expected-output files, and explain why reordering rows changes `iloc` results but not an exact `loc` identity request. The tests cover values, shapes, ordering, exceptions, duplicate labels, source preservation, and empty valid inputs.
