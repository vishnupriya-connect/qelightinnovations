# Randomness basics

## Create a sequence that you can repeat

**Randomness** means an outcome is not known in advance for a real trial. A computer often makes a **pseudo-random value** instead: a deterministic algorithm creates values that look variable. NumPy's **pseudo-random number generator** keeps an internal state and advances it whenever a value is drawn. The result of successive calls is a **random sequence** for simulations or practice data.

```python
import numpy as np

rng = np.random.default_rng(42)
first = rng.random(3)
second = rng.random(3)
print(first.shape, second.shape) # (3,) (3,)
```

`np.random` is NumPy's randomness namespace. `default_rng()` constructs a new **random generator**. Here `.random(3)` asks it for three floating-point values in `[0, 1)`. The individual numbers are less important than their sequence behavior; their sampling details come in the next lesson. The second call continues from the generator's current **random state** rather than restarting.

The number 42 passed to `default_rng()` is a **seed**, also called a **random seed**. It fixes the initial state for a repeatable run:

```python
left = np.random.default_rng(42)
right = np.random.default_rng(42)
print(np.array_equal(left.random(3), right.random(3))) # True
print(np.array_equal(left.random(3), right.random(3))) # True
```

The same seed *and the same sequence of calls* produce matching draws in the same NumPy setup. This is a **reproducible random sequence** useful for debugging. A seed is not a promise that the printed values remain identical across every NumPy version or generator algorithm; record the environment when exact long-term replay matters. Do not treat a fixed seed as cryptographic unpredictability.

## Calls advance state

Two fresh generators with the same seed have separate state even when their sequences initially match:

```python
a = np.random.default_rng(7)
b = np.random.default_rng(7)
first_a = a.random()
first_b = b.random()
a.random()                  # advances only a
next_b = b.random()         # b is now at its second value
reference = np.random.default_rng(7)
reference.random()          # consume its first value
print(first_a == first_b)          # True
print(next_b == reference.random()) # True
```

Each object is an **independent random generator** in the practical sense that advancing one does not advance the other's state. *Using the same seed still gives them identical streams when called alike.* If separate simulations need distinct streams, create separate generator seeds. NumPy's `SeedSequence.spawn()` can derive child seed sequences from one root:

```python
root = np.random.SeedSequence(2026)
child_a, child_b = root.spawn(2)
sim_a = np.random.default_rng(child_a)
sim_b = np.random.default_rng(child_b)
print(sim_a is sim_b) # False
```

The child generators have separate derived initial states. Recreating the root from 2026 and spawning children in the same way reproduces those streams in the same setup. Avoid repeatedly calling `np.random.default_rng(42)` inside a loop when you intend successive values: each new generator starts again at its first draw.

| Action | What happens |
| --- | --- |
| `rng = np.random.default_rng(42)` | Make a generator at the initial state set by seed 42 |
| `rng.random(3)` | Draw three values and advance `rng`'s state |
| `rng.random(3)` again | Draw the next three values |
| `np.random.default_rng(42)` again | Make a separate generator starting at the same initial state |
| `np.random.default_rng()` | Make a new generator with a fresh seed from the environment |

## Save a state for an exact replay within one run

The seed describes how to *start* a sequence. A state records where a generator is *now*. For a brief replay demonstration, copy its state before drawing:

```python
from copy import deepcopy

rng = np.random.default_rng(11)
rng.random(2)  # advance past the initial two values
saved = deepcopy(rng.bit_generator.state)
observed = rng.random(3)
rng.bit_generator.state = saved
replayed = rng.random(3)
print(np.array_equal(observed, replayed)) # True
```

The state belongs to the generator's underlying algorithm. `deepcopy` preserves this snapshot separately from later changes. Restoring state is useful for controlled debugging, but normal programs can usually recreate a generator from a recorded seed and repeated call order. Do not edit the contents of the state dictionary by hand.

## Guided lab

Download [Randomness basics lab](QAI.02.02.28_Randomness_Basics_Lab.zip), extract it, and run inside the folder:

```bash
python -m pip install -r requirements.txt
python randomness_basics.py
python check_randomness_basics.py
```

The program demonstrates matching sequences, separate generator states, spawned children, and saved-state replay. It prints Boolean checks rather than relying on a particular version's sample values. The checker reports `All checks passed.`

**Trace before running:** two fresh generators seeded 42 will agree on their first three values and next three values when called in the same order. Advancing only one cannot advance the other. Predict which calls match before viewing the checks.

**Controlled variation:** create generators `x` and `y` from seed 42. Draw four values from `x`, but only three from `y`. A fresh `reference` with seed 42 can draw three values and then one value; that fourth reference draw matches `x`'s fourth value. `y`'s next draw also matches it. This shows that grouping calls can differ while positions in the sequence are tracked.

**Debug:** If two same-seed runs disagree, check call order and sizes before suspecting the seed. If a loop prints the same first value repeatedly, move generator construction before the loop. If two same-seed generator objects produce matching values, that is expected; use distinct spawned child seeds when truly separate streams are required.

## Independent mini-project: reproducible trial log

Create two generator objects with seed 31. Draw three values from each and report whether they match. Advance only the first generator by one value. Verify the second generator's next value with a fresh reference generator advanced by three draws. Then snapshot the second generator's state, draw two values, restore the state, and verify those two values replay exactly. Print shapes and Boolean checks. The lab contains `mini_project_reference.py`.

Expected output, without depending on the numeric draws:

```text
first shapes (3,) (3,)
first match True
second position matches reference True
saved state replays True
separate objects True
```

Full reference solution:

```python
from copy import deepcopy
import numpy as np

first = np.random.default_rng(31)
second = np.random.default_rng(31)
draw_a = first.random(3)
draw_b = second.random(3)
first.random()  # only first advances
next_b = second.random()
reference = np.random.default_rng(31)
reference.random(3)
expected_next = reference.random()
saved = deepcopy(second.bit_generator.state)
observed = second.random(2)
second.bit_generator.state = saved
replayed = second.random(2)
print("first shapes", draw_a.shape, draw_b.shape)
print("first match", np.array_equal(draw_a, draw_b))
print("second position matches reference", next_b == expected_next)
print("saved state replays", np.array_equal(observed, replayed))
print("separate objects", first is not second)
```

## Check your understanding

1. **What does the seed set?** The generator's initial state, so the same sequence of calls can be reproduced in the same setup.
2. **Do two generators with the same seed share one state object?** No. Each advances separately, even though equal call sequences give equal draws.
3. **What changes after a draw?** The generator's random state, so a later call continues along the sequence.
4. **Why might a same-seed run produce different values in another environment?** Generator implementations and versions can change; record the setup for exact replay.

Remember: construct a generator once per intended stream, record its seed and call order, and distinguish separate state objects from distinct random streams.

## Further reading

- [NumPy: random Generator](https://numpy.org/doc/stable/reference/random/generator.html)
- [NumPy: default_rng](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.default_rng)
- [NumPy: parallel random number generation](https://numpy.org/doc/stable/reference/random/parallel.html)
