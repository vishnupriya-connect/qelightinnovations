# Simulation

## Model a trial, then repeat it

Suppose we want to estimate how often a fair six-sided die shows an even number. A **simulation** uses a computer model to imitate the experiment. One die roll is a **trial**; using a random generator to imitate that roll makes it a **random trial**. A collection of generated rolls is a **simulated sample**:

```python
import numpy as np

rng = np.random.default_rng(42)
rolls = rng.integers(1, 7, size=12)
even = rolls % 2 == 0
even_count = int(np.sum(even))
estimate = even_count / rolls.size
print(rolls.shape, even.shape) # (12,) (12,)
print(0 <= estimate <= 1)      # True
```

The generator draws integers from 1 inclusive to 7 exclusive, so a simulated roll is 1 through 6. `% 2 == 0` marks values divisible by two. The **simulated experiment** is the full procedure: draw rolls, mark even ones, and summarize. Its **simulation inputs** are the die model, the number of rolls, the event rule, and the seed; its **simulation outputs** are the rolls, the success count, and the estimated fraction. The count and estimate vary with the generated sample.

For a visible calculation, imagine one sample happens to be `[1, 2, 6, 3, 4, 5]`. Three of six rolls are even. Its observed **empirical frequency** is a count of 3, and its *relative* empirical frequency is `3/6 = 0.5`. This relative frequency is the **estimated probability** from that sample. Under the assumed fair model, the exact mathematical probability is also `3/6 = 0.5`, because three of the six equally likely faces are even. A different six-roll sample need not produce exactly 0.5.

## One run versus repeated simulation

A **simulation run** is one batch of trials with one set of inputs. We can do several runs to see how much estimates vary:

```python
def run_even_die(n, rng):
    if n <= 0:
        raise ValueError("Number of trials must be positive")
    rolls = rng.integers(1, 7, size=n)
    successes = int(np.sum(rolls % 2 == 0))
    return rolls, successes, successes / n

rng = np.random.default_rng(19)
for run_number in range(3):
    rolls, count, fraction = run_even_die(12, rng)
    print(run_number + 1, count, round(fraction, 3))
```

This is **repeated simulation**: three successive, separate 12-roll batches. The same generator advances after each batch, so they are not three copies of the identical first batch. The **simulation result** for each run includes its count and fraction. A small batch can show a fraction far from 0.5; larger batches tend to make a more stable estimate in the long run, but any particular larger run is not guaranteed to be closer than every smaller one.

| Part | Die example |
| --- | --- |
| Model | Six equally likely faces, numbered 1 through 6 |
| Trial | Generate one face |
| Event | Face is even |
| Run | Generate `n` faces and count even ones |
| Empirical count | Number of even faces observed |
| Relative frequency / estimate | Even count divided by `n` |

## Reproduce a run without freezing the conclusion

A **fixed random seed** makes the same call sequence repeat in the same NumPy setup:

```python
first = run_even_die(12, np.random.default_rng(42))
replay = run_even_die(12, np.random.default_rng(42))
print(np.array_equal(first[0], replay[0])) # True
print(first[1:] == replay[1:])             # True
```

This is **simulation reproducibility**. It helps debug a procedure, not establish that the observed fraction is the true probability. Changing the seed changes the sampled run in general; a different seed could also happen to produce the same small result. The exact draw stream is not guaranteed across all future NumPy versions, so record the environment if byte-for-byte replay matters.

Keep the model separate from the code. If the physical die is biased, the fair generator model does not magically describe it. If the event changes from “even” to “at least 5,” recompute the condition on the *same rolls* when you want to compare event rules without changing the sample.

## Guided lab

Download [Simulation lab](QAI.02.02.30_Simulation_Lab.zip), extract it, and run inside the folder:

```bash
python -m pip install -r requirements.txt
python simulation.py
python check_simulation.py
```

The program shows one batch and three repeated batches. The checker verifies range, counts, fractions, seed replay, and an invalid zero-trial request; it reports `All checks passed.`

**Trace before running:** in the illustrative sample `[1, 2, 6, 3, 4, 5]`, mark even faces `[False, True, True, False, True, False]`, then calculate count 3 and relative frequency 0.5.

**Controlled variation:** keep a generated `rolls` array fixed. Compare the event “even” with “at least 5” by evaluating `rolls % 2 == 0` and `rolls >= 5` on that same array. Report each count and fraction; do not assume either event has the larger empirical fraction in a short run. The fair-model probabilities are 3/6 and 2/6, respectively.

**Debug:** If an estimated probability exceeds 1, check that you divided the success count by the number of trials rather than by an unrelated quantity. If two same-seed runs disagree, inspect the number and order of generator calls. If a zero-trial run attempts to divide by zero, reject it before drawing.

## Independent mini-project: simulate coin tosses

Represent a fair coin by integers 0 (tails) and 1 (heads). With one generator seeded 31, perform three runs of 20 tosses each. For each run, print the number of tosses, heads count, and estimated probability of heads. Then report the overall heads count, total tosses, and combined estimate. Replay with a second generator seeded 31 and check that all three generated samples match. Print Boolean checks and shapes instead of fixed sample counts in your summary so the expected output is independent of NumPy's particular draws. The lab contains `mini_project_reference.py`.

Expected summary form:

```text
run shapes [(20,), (20,), (20,)]
counts valid True
total tosses 60
combined estimate valid True
same-seed replay True
```

Full reference solution:

```python
import numpy as np

def coin_runs(seed, runs=3, tosses_per_run=20):
    rng = np.random.default_rng(seed)
    samples = []
    for run_number in range(runs):
        tosses = rng.integers(0, 2, size=tosses_per_run)
        heads = int(np.sum(tosses == 1))
        fraction = heads / tosses_per_run
        print("run", run_number + 1, "tosses", tosses.size,
              "heads", heads, "estimate", round(fraction, 3))
        samples.append(tosses)
    return samples

samples = coin_runs(31)
replay = coin_runs(31)
total_heads = sum(int(np.sum(tosses == 1)) for tosses in samples)
total_tosses = sum(tosses.size for tosses in samples)
combined = total_heads / total_tosses
print("run shapes", [tosses.shape for tosses in samples])
print("counts valid", all(0 <= int(np.sum(t == 1)) <= t.size for t in samples))
print("total tosses", total_tosses)
print("combined estimate valid", 0 <= combined <= 1)
print("same-seed replay",
      all(np.array_equal(a, b) for a, b in zip(samples, replay)))
```

The three per-run lines include sampled counts and fractions; these need not be memorized. The combined estimate uses all 60 tosses rather than treating one run as the entire experiment.

## Check your understanding

1. **What is one trial in the die simulation?** One generated face from 1 through 6.
2. **How do you estimate the probability of an event?** Divide its observed count by the number of trials.
3. **Does a six-roll result of 0.5 prove the die is fair?** No. It is a sample fraction, and many models can produce that outcome.
4. **Why does a fixed seed help?** The same procedure and call order can replay a run for checking and debugging in the same setup.
5. **Why use one generator for three successive runs?** Its state advances, so each run receives a new batch from the sequence.

Remember: define the model, event, trial count, and seed; compute the observed fraction; then interpret it as an estimate under those assumptions.

## Further reading

- [NumPy: random Generator](https://numpy.org/doc/stable/reference/random/generator.html)
- [NumPy: Generator.integers](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.integers.html)
- [Penn State: understanding uncertainty and simulation](https://online.stat.psu.edu/stat100/Lesson07)
