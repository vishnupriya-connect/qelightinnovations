# Random sampling

## Draw items from a known population

A **population** is the full set of items eligible for a draw. A **sample** is the selected collection; each selected entry is a **sample item**. The **sample size** is the number of selected entries:

```python
import numpy as np

population = np.array([10, 20, 30, 40])
rng = np.random.default_rng(2026)
sample = rng.choice(population, size=3, replace=False)
print(sample.shape) # (3,)
print(np.all(np.isin(sample, population))) # True
print(np.unique(sample).size == 3) # True
```

`rng.choice()` makes a **random choice** from the population. With `replace=False`, this is a **sample without replacement**: a selected position cannot be selected again in that draw. Because this population's values are unique, the three sample values are also unique. If the population itself contains duplicate values, distinct selected *positions* can still have equal values. Without replacement, a size larger than the population's number of items raises `ValueError`.

With `replace=True`, the item returns to the pool before the next selection: this is a **sample with replacement**, and repeats are allowed:

```python
with_replacement = rng.choice(population, size=6, replace=True)
print(with_replacement.shape) # (6,)
print(np.unique(with_replacement).size < 6) # True: six draws from four unique values
```

This is a **random sample** in the sense that the generator selects items according to its sampling rule. The printed draw depends on seed, call order, and NumPy setup; the important properties above do not depend on a particular drawn sequence.

## Draw integer and floating-point values

`rng.integers(1, 7, size=5)` produces **random integers** from 1 through 6. The lower bound is included; the upper bound 7 is excluded:

```python
dice = rng.integers(1, 7, size=5)
print(dice.shape, np.all((dice >= 1) & (dice < 7))) # (5,) True
```

`rng.random(5)` produces **random floating-point numbers** from 0 inclusive up to, but not including, 1:

```python
fractions = rng.random(5)
print(fractions.shape, np.all((fractions >= 0) & (fractions < 1)))
# (5,) True
```

These are examples of a **uniform distribution**: eligible values or equal-length parts of the range have equal selection chances under the model. That describes the generator's sampling rule, not a guarantee that a short sample will contain every value or look evenly spaced. The draws are pseudo-random, as explained in the previous lesson.

## Draw from a normal distribution

A **normal distribution** has a bell-shaped pattern centered on a mean. `rng.normal(loc=50, scale=10, size=5)` requests five values around center 50 with standard deviation parameter 10:

```python
normal_values = rng.normal(loc=50, scale=10, size=5)
print(normal_values.shape) # (5,)
```

`loc` is the center and `scale` is the positive spread parameter. A five-value sample is not guaranteed to have mean exactly 50, nor to stay within any fixed interval such as 40 through 60. A normal model can produce values far from its center; choose it only when that model suits the quantity. Its output is floating-point, even if `loc` is written as an integer.

| Method | What it samples | Shape here | Key rule |
| --- | --- | --- | --- |
| `rng.integers(1, 7, size=5)` | integers | `(5,)` | 1 included, 7 excluded |
| `rng.random(5)` | uniform floats | `(5,)` | `[0, 1)` |
| `rng.normal(50, 10, size=5)` | normal floats | `(5,)` | center 50, spread 10; no hard bounds |
| `rng.choice(population, size=3, replace=False)` | population items | `(3,)` | no repeated selected positions |
| `rng.choice(population, size=6, replace=True)` | population items | `(6,)` | repeated positions allowed |

## Permute a copy or shuffle in place

A **random permutation** rearranges all items, keeping every item exactly once. `rng.permutation()` returns a rearranged copy of an array; `rng.shuffle()` rearranges an existing array in place and returns `None`:

```python
original = np.array([10, 20, 30, 40])
permuted = rng.permutation(original)
editable = original.copy()
returned = rng.shuffle(editable)
print(np.array_equal(np.sort(permuted), np.sort(original))) # True
print(np.array_equal(np.sort(editable), np.sort(original))) # True
print(returned, original.tolist()) # None [10, 20, 30, 40]
```

The two randomized orders need not match because each call advances the generator. A valid permutation can occasionally equal the original order by chance. Do not check that the order *must* change; check that all original items remain present. `shuffle()` changes `editable`, so copy first when preserving the source matters. For a two-dimensional array, the default shuffle acts along the first axis (reordering rows), not individual cells.

## Guided lab

Download [Random sampling lab](QAI.02.02.29_Random_Sampling_Lab.zip), extract it, and run in the folder:

```bash
python -m pip install -r requirements.txt
python random_sampling.py
python check_random_sampling.py
```

The program shows every method with a seeded generator and prints shape and validity checks. The checker verifies replay, ranges, population membership, replacement behavior, permutation membership, and in-place mutation rules; it prints `All checks passed.`

**Trace before running:** a size-3 sample without replacement from four distinct items cannot repeat a value. A size-6 sample with replacement from those same four items *must* contain a repeated value. A permutation keeps four items; it does not make a smaller sample.

**Controlled variation:** change the choice sample size from 3 to 4 while keeping `replace=False`; all four distinct population items appear once, in a drawn order. Try size 5 with `replace=False` and observe `ValueError`. With `replace=True`, a size of 5 is allowed.

**Debug:** If a simulated die shows 0 or never allows 6, inspect the arguments to `integers()`; use `(1, 7)` for values 1 through 6. If `x = rng.shuffle(x)` makes `x` become `None`, call `rng.shuffle(x)` separately or use `x = rng.permutation(x)` for a copy. If a fixed seed does not replay, check the order and sizes of *every* preceding generator call.

## Independent mini-project: practice question bank

Use question IDs `questions = np.array([101, 102, 103, 104])` and a generator seeded 31. Draw eight die results from 1 through 6, five uniform floats, five normal floats centered at 10 with spread 2, six question IDs with replacement, three without replacement, a permutation of all four IDs, and a separate copied array shuffled in place. Print only shapes and Boolean validity checks so the expected output is independent of the sampled numbers. The lab contains `mini_project_reference.py`.

Expected output:

```text
dice (8,) True
uniform (5,) True
normal (5,)
with replacement (6,) True True
without replacement (3,) True True
permutation (4,) True
shuffle (4,) True None
original [101, 102, 103, 104]
```

For the replacement line, the first `True` means every result belongs to the population; the second means six draws from four unique values necessarily repeat. The full reference solution is:

```python
import numpy as np

questions = np.array([101, 102, 103, 104])
rng = np.random.default_rng(31)
dice = rng.integers(1, 7, size=8)
uniform = rng.random(5)
normal = rng.normal(loc=10, scale=2, size=5)
with_replacement = rng.choice(questions, size=6, replace=True)
without_replacement = rng.choice(questions, size=3, replace=False)
permutation = rng.permutation(questions)
shuffled = questions.copy()
returned = rng.shuffle(shuffled)
print("dice", dice.shape, bool(np.all((dice >= 1) & (dice < 7))))
print("uniform", uniform.shape, bool(np.all((uniform >= 0) & (uniform < 1))))
print("normal", normal.shape)
print("with replacement", with_replacement.shape,
      bool(np.all(np.isin(with_replacement, questions))),
      np.unique(with_replacement).size < with_replacement.size)
print("without replacement", without_replacement.shape,
      bool(np.all(np.isin(without_replacement, questions))),
      np.unique(without_replacement).size == without_replacement.size)
print("permutation", permutation.shape,
      bool(np.array_equal(np.sort(permutation), np.sort(questions))))
print("shuffle", shuffled.shape,
      bool(np.array_equal(np.sort(shuffled), np.sort(questions))), returned)
print("original", questions.tolist())
```

## Check your understanding

1. **What is a population, and what is a sample?** The population is the eligible set; the sample is the selected items.
2. **Can `replace=False` choose five positions from a four-item population?** No. Without replacement, each position can be chosen once at most.
3. **What integers can `rng.integers(1, 7)` return?** 1 through 6; the upper limit 7 is excluded.
4. **Does a normal sample of five values necessarily average to `loc`?** No. `loc` describes the distribution center, not an exact outcome for a short sample.
5. **Which changes its input: `permutation()` or `shuffle()`?** `shuffle()` changes the supplied array in place; `permutation()` returns a rearranged copy.

Remember: specify the population, size, replacement rule, and distribution before drawing; verify properties instead of expecting one particular sequence.

## Further reading

- [NumPy: random Generator](https://numpy.org/doc/stable/reference/random/generator.html)
- [NumPy: integers](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.integers.html), [random](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.random.html), and [normal](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.normal.html)
- [NumPy: choice](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.choice.html), [permutation](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.permutation.html), and [shuffle](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.shuffle.html)
