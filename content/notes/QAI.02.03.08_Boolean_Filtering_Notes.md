# Boolean filtering

Boolean filtering keeps rows whose conditions evaluate to `True`. It turns a requirement such as “show active Python or SQL learners with a score of at least 80” into a visible, testable selection rule.

You should already know DataFrame columns and label selection. This lesson develops comparison masks, combined conditions, membership and missing-value filters, index alignment, predictable failure handling, and a validated mini-project.

[Runnable lab ZIP](QAI.02.03.08_Boolean_Filtering_Lab.zip) · [Scripts and README](QAI.02.03.08_resources/README.md)

## Core vocabulary and mental model

A **filter** selects a subset of rows. A **filter condition** is a rule evaluated for every row. A condition such as `df['score'] >= 80` compares each value with `80` and returns a **Boolean Series**: a one-dimensional labelled object containing `True` and `False` values. Used for selection, that Series is a **Boolean mask**.

Think of a mask as a row-by-row gate:

- `True` opens the gate and keeps the row.
- `False` closes the gate and removes the row.
- each mask label identifies the row whose gate it controls.

Filtering does not normally change the source DataFrame. It produces a new selected object.

## Working table

```python
import pandas as pd

df = pd.DataFrame(
    {
        'learner': ['Anu', 'Bala', 'Chitra', 'Deepa', 'Eshan', 'Farah'],
        'track': ['Python', 'SQL', 'Python', 'Cloud', 'SQL', 'Python'],
        'score': [72, 85, 91, 68, 88, 80],
        'attempts': [1, 2, 1, 3, 2, 1],
        'mentor': ['Mira', None, 'Ravi', 'Mira', pd.NA, 'Ravi'],
        'active': [True, True, True, False, True, True],
    },
    index=['L10', 'L20', 'L30', 'L40', 'L50', 'L60'],
)
```

| label | learner | track | score | attempts | mentor | active |
|---|---|---|---:|---:|---|---|
| L10 | Anu | Python | 72 | 1 | Mira | True |
| L20 | Bala | SQL | 85 | 2 | missing | True |
| L30 | Chitra | Python | 91 | 1 | Ravi | True |
| L40 | Deepa | Cloud | 68 | 3 | Mira | False |
| L50 | Eshan | SQL | 88 | 2 | missing | True |
| L60 | Farah | Python | 80 | 1 | Ravi | True |

The index is the mask's alignment key. The mask values decide whether the corresponding labels survive.

## One comparison condition

```python
mask = df['score'] >= 80
print(type(mask).__name__)
print(mask.dtype)
print(mask.tolist())
print(df.loc[mask, ['learner', 'score']].to_csv(index=True).strip())
```

Expected output:

```text
Series
bool
[False, True, True, False, True, True]
,learner,score
L20,Bala,85
L30,Chitra,91
L50,Eshan,88
L60,Farah,80
```

The comparison is vectorised: Pandas applies `>= 80` to the entire score Series. The mask has the same labels as the source. `loc` retains rows whose aligned values are `True` and keeps their original order.

Comparison filters include:

- equality: `df['track'] == 'Python'`;
- inequality: `df['track'] != 'Cloud'`;
- greater than: `df['score'] > 80`;
- less than: `df['attempts'] < 2`;
- inclusive comparisons: `>=` and `<=`.

Use `==`, not assignment operator `=`, inside a comparison.

## Logical and, or, and not

For Pandas masks use element-wise operators:

- `&` means logical **and**: keep a row only when both conditions are true.
- `|` means logical **or**: keep a row when either condition is true.
- `~` means logical **not**: invert each Boolean value.

```python
and_mask = (df['score'] >= 80) & (df['attempts'] == 1)
or_mask = (df['track'] == 'SQL') | (df['score'] > 90)
not_mask = ~(df['track'] == 'Cloud')

print(df.index[and_mask].tolist())
print(df.index[or_mask].tolist())
print(df.index[not_mask].tolist())
```

Expected output:

```text
['L30', 'L60']
['L20', 'L30', 'L50']
['L10', 'L20', 'L30', 'L50', 'L60']
```

Python's scalar words `and`, `or`, and `not` try to reduce an entire Series to one truth value. A Series has many truth values, so that request is ambiguous and raises `ValueError`. Use `&`, `|`, and `~` for element-wise mask operations.

## Condition grouping and parentheses

Every comparison must be parenthesised before combining masks:

```python
mask = (df['active']) & ((df['track'] == 'Python') | (df['track'] == 'SQL'))
```

Parentheses express the intended order: first create the two track masks, combine them with `|`, then combine that result with the active mask using `&`.

Without parentheses, Python's operator precedence can group operands in an unintended way. For example, `df['score'] >= 80 & df['attempts'] == 1` is not interpreted as two complete comparisons joined by `&`. It may raise a type or ambiguous-truth error, or compute an unintended intermediate result. Parenthesised conditions are both correct and readable.

## Membership filtering with `isin()`

A **membership filter** asks whether each value belongs to an allowed collection. `isin()` returns a Boolean object of the same shape as its caller.

```python
allowed_tracks = ['Python', 'SQL']
mask = df['track'].isin(allowed_tracks)
print(mask.tolist())
print(df.loc[mask, 'learner'].tolist())
```

Expected output:

```text
[True, True, True, False, True, True]
['Anu', 'Bala', 'Chitra', 'Eshan', 'Farah']
```

This is clearer and easier to extend than chaining many equality comparisons. To express “not in,” invert the mask: `~df['track'].isin(allowed_tracks)`.

`isin()` tests exact membership. It does not perform substring, regular-expression, fuzzy, or case-insensitive matching. `'python'` does not match `'Python'` unless values are deliberately normalised first.

## Missing and non-missing filters

A **null filter** identifies missing values. `isna()` maps recognised missing values such as `None`, `NaN`, `pd.NA`, and `NaT` to `True`. A **non-null filter** uses `notna()` to map existing values to `True`.

```python
print(df.index[df['mentor'].isna()].tolist())
print(df.index[df['mentor'].notna()].tolist())
```

Expected output:

```text
['L20', 'L50']
['L10', 'L30', 'L40', 'L60']
```

Do not test missing values with `== None`, `== pd.NA`, or `== float('nan')`. Missing sentinels have special comparison semantics; `isna()` and `notna()` state the requirement directly. An empty string is not automatically missing.

## Selecting columns while filtering rows

`df.loc[row_mask, column_labels]` makes both axes explicit:

```python
result = df.loc[
    (df['active']) & (df['score'] >= 80),
    ['learner', 'track', 'score'],
]
print(result.to_csv(index=True).strip())
```

Expected output:

```text
,learner,track,score
L20,Bala,SQL,85
L30,Chitra,Python,91
L50,Eshan,SQL,88
L60,Farah,Python,80
```

The comma separates row selection from column selection. Filtering affects rows; the list establishes the output fields and their order.

## Label alignment: the mask is not only a list of booleans

A Boolean Series carries labels. `loc` aligns the mask to the DataFrame index before selection:

```python
reordered = pd.Series(
    [True, False, True, False, False, False],
    index=['L60', 'L50', 'L40', 'L30', 'L20', 'L10'],
)
print(df.loc[reordered, 'learner'].tolist())
```

Expected output:

```text
['Deepa', 'Farah']
```

The first `True` belongs to `L60`, not source position 0. The other `True` belongs to `L40`. Selection returns source order, so Deepa precedes Farah.

If a Boolean Series lacks required source labels, Pandas raises an unalignable-mask `IndexingError`. Extra labels are ignored only after every source label can be aligned. For reliable code, derive masks from the same DataFrame or explicitly verify `mask.index.equals(df.index)` when exact order and membership are part of the contract.

A plain Boolean array has no labels, so it is interpreted positionally and must have exactly the same length as the axis. Prefer labelled masks when row identity matters.

## Nullable Boolean masks

Pandas also has a nullable `boolean` dtype whose values can be `True`, `False`, or `pd.NA`. During Boolean indexing, an `NA` mask entry is treated as `False`:

```python
nullable = pd.Series(
    [True, pd.NA, False, True, False, True],
    index=df.index,
    dtype='boolean',
)
print(df.loc[nullable, 'learner'].tolist())
```

Expected output:

```text
['Anu', 'Deepa', 'Farah']
```

That default may silently exclude an unknown decision. Choose the policy deliberately. Use `nullable.fillna(False)` to exclude unknowns explicitly, `fillna(True)` to retain them for review, or reject masks containing unknowns when the decision must be complete.

## Deliberate failures and debugging

### Failure 1: scalar logical operator

```python
df[(df['score'] >= 80) and (df['active'])]
```

Typical result: `ValueError: The truth value of a Series is ambiguous...`

Resolution: use `(condition_one) & (condition_two)`.

### Failure 2: missing parentheses

```python
df['score'] >= 80 & df['attempts'] == 1
```

Resolution: make each comparison complete: `(df['score'] >= 80) & (df['attempts'] == 1)`.

### Failure 3: wrong mask length

```python
df.loc[[True, False]]
```

Typical result: `IndexError` because a two-value positional mask cannot control six rows.

Resolution: generate the mask from the source or verify its length.

### Failure 4: unalignable labels

```python
bad = pd.Series([True, False], index=['X', 'Y'])
df.loc[bad]
```

Typical result: `IndexingError` because source labels cannot be aligned.

Resolution: use a mask with exactly the intended source labels; do not discard labels merely to suppress the error.

Debug a filter in stages:

1. print each component mask separately;
2. inspect `dtype`, length, labels, and missing mask values;
3. count matches with `int(mask.fillna(False).sum())`;
4. inspect kept labels with `df.index[mask.fillna(False)].tolist()`;
5. combine only after each component matches the plain-language requirement;
6. test boundary, missing, empty, and no-match cases.

## Solved mechanism trace

Trace this condition:

```python
(df['active']) & (df['track'].isin(['Python', 'SQL'])) & (df['score'] >= 80)
```

For `L10`, the three values are `True`, `True`, and `False`; the result is `False`.

For `L20`, they are `True`, `True`, and `True`; the result is `True`.

For `L30`, they are `True`, `True`, and `True`; the result is `True`.

For `L40`, they are `False`, `False`, and `False`; the result is `False`.

For `L50`, they are `True`, `True`, and `True`; the result is `True`.

For `L60`, they are `True`, `True`, and `True`; the result is `True`.

The final mask is `[False, True, True, False, True, True]`, retaining `L20`, `L30`, `L50`, and `L60`.

## Guided runnable lab

From the resource directory, run:

```bash
python -m pip install -r requirements.txt
python lab.py
python project.py
python -m unittest -v test_project.py
```

Before each output, predict the mask values and retained labels. The lab demonstrates comparison, and/or/not, membership, null, aligned reordered, and nullable masks. It catches four deliberate failures and prints their exception classes so execution continues. Compare the output byte-for-byte with `expected_lab.txt`.

## Controlled variation with solution

Requirement: select active Python learners whose score is below 90 or whose mentor is missing; return learner, score, and mentor.

```python
variation_mask = (
    (df['active'])
    & (df['track'] == 'Python')
    & ((df['score'] < 90) | (df['mentor'].isna()))
)
variation = df.loc[variation_mask, ['learner', 'score', 'mentor']]
print(variation.to_csv(index=True).strip())
```

Expected output:

```text
,learner,score,mentor
L10,Anu,72,Mira
L60,Farah,80,Ravi
```

Chitra is active and in Python, but her score is not below 90 and her mentor is present. The inner parentheses ensure the `or` rule remains one grouped part of the larger `and` rule.

## Independent mini-project: validated review queue

Build `build_review_queue(source, allowed_tracks, minimum_score, include_unassigned=False)`. It must:

- require columns `learner`, `track`, `score`, `mentor`, and `active`;
- require unique row labels;
- reject an empty track collection and repeated tracks;
- reject Boolean and non-numeric thresholds;
- require numeric, non-missing scores and Boolean `active` values;
- keep active rows in an allowed track with score at least the threshold;
- exclude missing mentors by default or retain them when `include_unassigned=True`;
- return exactly `learner`, `track`, `score`, and `mentor` in source order;
- return an independent copy without mutating the source.

Complete reference solution:

```python
from numbers import Real
import pandas as pd


def build_review_queue(source, allowed_tracks, minimum_score, include_unassigned=False):
    required = ['learner', 'track', 'score', 'mentor', 'active']
    missing = [name for name in required if name not in source.columns]
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    if not source.index.is_unique:
        raise ValueError('Source row labels must be unique')

    tracks = list(allowed_tracks)
    if not tracks:
        raise ValueError('allowed_tracks must not be empty')
    if len(tracks) != len(set(tracks)):
        raise ValueError('allowed_tracks must not contain duplicates')
    if isinstance(minimum_score, bool) or not isinstance(minimum_score, Real):
        raise TypeError('minimum_score must be a real number')
    if not isinstance(include_unassigned, bool):
        raise TypeError('include_unassigned must be Boolean')
    if not pd.api.types.is_numeric_dtype(source['score']):
        raise TypeError('score must be numeric')
    if source['score'].isna().any():
        raise ValueError('score must not contain missing values')
    if not pd.api.types.is_bool_dtype(source['active']):
        raise TypeError('active must be Boolean')

    mask = (
        source['active']
        & source['track'].isin(tracks)
        & source['score'].ge(minimum_score)
    )
    if not include_unassigned:
        mask &= source['mentor'].notna()

    return source.loc[mask, ['learner', 'track', 'score', 'mentor']].copy()
```

For the working data, `project.py` uses tracks Python and SQL, minimum score 80, and includes unassigned learners. Expected output:

```text
,learner,track,score,mentor
L20,Bala,SQL,85,
L30,Chitra,Python,91,Ravi
L50,Eshan,SQL,88,
L60,Farah,Python,80,Ravi
```

The tests cover the exact result, default exclusion of missing mentors, boundary inclusion, no matches, source order, track membership, missing columns, duplicate labels, empty and duplicate track lists, invalid thresholds and flags, non-numeric or missing scores, invalid active dtype, and source/result independence.

## Assumptions, limitations, and trade-offs

- A correct mask can still encode the wrong business rule. Translate the requirement explicitly and test boundary cases.
- Exact string membership is sensitive to spelling, case, and whitespace. Validate or normalise categories before filtering, not silently during every query.
- Missing mask decisions need a stated policy; automatic exclusion may hide records requiring review.
- Label alignment protects row identity but can make an externally constructed mask surprising. Deriving masks from the same source reduces this risk.
- Boolean filtering scans the relevant values. For data larger than memory, use database, chunked, or distributed filtering and validate equivalent semantics.
- Returning a copy costs memory but makes downstream editing intent clearer. Object-valued cells can still contain shared Python objects.
- Filtering sensitive data reduces rows in the result but does not anonymise retained values or secure the source.
- A threshold such as 80 assumes scores are comparable, correctly typed, and measured under the same policy.

## Solved recall, implementation, and decision questions

**What does a Boolean mask contain?** One row decision per label: normally `True` to keep and `False` to exclude.

**Why use `&` instead of `and`?** `&` combines values element by element. `and` asks for one truth value from each whole Series, which is ambiguous.

**Why parenthesise every comparison?** Comparison and bitwise operator precedence otherwise permits unintended grouping before mask combination.

**How do you express “track is Python or SQL”?** `df['track'].isin(['Python', 'SQL'])`.

**How do you express “track is neither Python nor SQL”?** `~df['track'].isin(['Python', 'SQL'])`.

**Why not use `df['mentor'] == None`?** Missing values have special representations and comparison behavior. `isna()` expresses the intended test consistently.

**What happens to `pd.NA` in a nullable Boolean indexing mask?** It is treated as `False` and the row is excluded unless the mask is filled or rejected under another explicit policy.

**Does a reordered Boolean Series select by mask position?** No. `loc` aligns its labels to source labels; returned rows remain in source order.

**What does an unalignable mask error protect against?** Applying decisions labelled for unrelated or incomplete rows to the source.

**How do you count selected rows before selecting?** For an ordinary Boolean mask use `int(mask.sum())`; for a nullable mask choose a missing policy first, such as `int(mask.fillna(False).sum())`.

**When is `query()` preferable?** It can make some interactive expressions readable, but explicit masks are easier to compose, inspect, reuse, and test, especially with dynamic inputs.

**What proves that the mini-project preserves the source?** Tests compare the source with a saved copy and edit the returned table, then verify the source did not change.

## Remember and teach back

- comparisons create labelled Boolean masks;
- `True` keeps a row and `False` removes it;
- use `&`, `|`, and `~`, with every comparison in parentheses;
- `isin()` performs exact membership filtering;
- `isna()` and `notna()` handle missingness;
- labelled masks align by index, while plain arrays act positionally;
- nullable `NA` decisions are excluded by default, so choose the policy explicitly;
- inspect component masks and test edge cases before trusting a combined rule.

Teach it aloud: “A filter is a labelled decision for each row. I build each condition separately, check its labels and values, combine complete comparisons with parenthesised `&`, `|`, or `~`, and use `isin`, `isna`, and `notna` for membership and missingness. I make unknown decisions explicit and test the rule's boundaries.”

Keep the exact lab output, passing tests, mini-project output, one deliberate-failure diagnosis, and a short teach-back explanation as evidence.

## References

- [Pandas: indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing)
- [Pandas: nullable Boolean data type](https://pandas.pydata.org/docs/user_guide/boolean.html)
- [Pandas: Series.isin](https://pandas.pydata.org/docs/reference/api/pandas.Series.isin.html)
- [Pandas: Series.isna](https://pandas.pydata.org/docs/reference/api/pandas.Series.isna.html)
- [Pandas: Series.notna](https://pandas.pydata.org/docs/reference/api/pandas.Series.notna.html)
