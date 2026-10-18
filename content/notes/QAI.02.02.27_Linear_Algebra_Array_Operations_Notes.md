# Linear-algebra array operations

## Multiply a matrix by a vector or another matrix

A **matrix** here is a two-dimensional NumPy array. Let each row describe an output and each column describe an input:

```python
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])
v = np.array([2.0, 1.0])
print((A @ v).tolist()) # [5.0, 4.0]
```

**Matrix multiplication** combines each row of `A` with the vector: the first output is `2×2 + 1×1 = 5`; the second is `1×2 + 2×1 = 4`. The `@` operator asks for this linear-algebra operation. The inner shape lengths must match: `(2, 2) @ (2,)` makes a `(2,)` result. It is a **matrix product** when the second operand is also a matrix:

```python
B = np.array([[1.0, 2.0], [3.0, 4.0]])
product = A @ B
print(product.tolist()) # [[5.0, 8.0], [7.0, 10.0]]
print(np.matmul(A, B).tolist()) # same result
```

The top-left element is row 0 of `A` paired with column 0 of `B`: `2×1 + 1×3 = 5`. For shapes `(m, n) @ (n, p)`, the result is `(m, p)`. `np.matmul()` performs the same matrix multiplication as `@` here. For these two-dimensional matrices, `np.dot(A, B)` also yields this product; the functions have different rules for some higher-dimensional inputs.

**Element-wise multiplication** instead pairs entries at the *same coordinates*:

```python
print((A * B).tolist()) # [[2.0, 2.0], [3.0, 8.0]]
```

At `[0, 0]`, `A * B` gives `2×1 = 2`, while `A @ B` gives 5. Do not substitute one for the other.

## Dot, inner, and outer products of vectors

For two one-dimensional vectors, a **dot product** multiplies matching entries and adds them. The **inner product** of these real vectors does the same:

```python
u = np.array([2.0, 1.0])
w = np.array([3.0, 4.0])
print(np.dot(u, w))   # 10.0: 2×3 + 1×4
print(np.inner(u, w)) # 10.0
print(np.outer(u, w).tolist())
# [[6.0, 8.0], [3.0, 4.0]]
```

The **outer product** creates every pairwise multiplication: two entries in `u` by two in `w` give a `(2, 2)` array. The examples use real one-dimensional vectors; avoid treating `inner`, `dot`, and `outer` as interchangeable for arbitrary array dimensions.

| Inputs | Operation | Output |
| --- | --- | --- |
| two vectors `(2,)` | `np.dot(u, w)` or `np.inner(u, w)` | scalar `10` |
| two vectors `(2,)` | `np.outer(u, w)` | matrix `(2, 2)` |
| matrix `(2, 2)` and vector `(2,)` | `A @ v` | vector `(2,)` |
| two matrices `(2, 2)` | `A @ B` or `np.matmul(A, B)` | matrix `(2, 2)` |
| two matrices `(2, 2)` | `A * B` | element-wise matrix `(2, 2)` |

## Solve a linear equation

`np.linalg` is NumPy's **linear algebra module**. The equation `A @ x = b` is a **linear equation** in unknown vector `x`; together its rows form a linear system:

```python
b = np.array([5.0, 4.0])
x = np.linalg.solve(A, b)
print(x.tolist())          # [2.0, 1.0]
print((A @ x).tolist())    # [5.0, 4.0]
```

The **linear-system solution** `x = [2, 1]` satisfies both equations, `2x₀ + x₁ = 5` and `x₀ + 2x₁ = 4`. The verification `A @ x` returns the requested right-hand side `b`. `solve()` is preferable to computing an inverse solely to solve such a system.

## Determinant, inverse, and rank

For a two-by-two matrix `[[a,b],[c,d]]`, its **determinant** is `a×d - b×c`. Our `A` has determinant `2×2 - 1×1 = 3`:

```python
print(round(float(np.linalg.det(A)), 6)) # 3.0
inverse = np.linalg.inv(A)
print(np.round(inverse, 3).tolist())
# [[0.667, -0.333], [-0.333, 0.667]]
print(np.allclose(A @ inverse, np.eye(2))) # True
print(np.linalg.matrix_rank(A)) # 2
```

An **inverse matrix** undoes multiplication by an invertible square matrix: `A @ inverse` is approximately the identity matrix `[[1,0],[0,1]]`, meaning no change to a vector. `np.eye(2)` creates that identity. The inverse's displayed decimals are rounded; compare floating-point results with `np.allclose()` rather than exact equality.

**Matrix rank** counts independent rows or columns. `A` has rank 2, so both rows contribute distinct information and its linear system has a unique solution. A determinant of zero for a square matrix signals no inverse:

```python
singular = np.array([[1.0, 2.0], [2.0, 4.0]])
print(round(float(np.linalg.det(singular)), 6)) # 0.0
print(np.linalg.matrix_rank(singular))           # 1
```

The second row is twice the first; it supplies no independent equation. `np.linalg.inv(singular)` and a `solve()` on it raise `np.linalg.LinAlgError`. For real measured matrices, a determinant near zero can also make an answer numerically fragile; do not assume a tiny nonzero computed value guarantees a reliable inverse.

## Eigenvalues and eigenvectors

An **eigenvector** is a nonzero direction `q` that a square matrix changes only by a scale. The scale is its **eigenvalue** `λ`: `A @ q = λ * q`. For this symmetric matrix, `[1, 1]` scales by 3 and `[1, -1]` scales by 1:

```python
print((A @ np.array([1.0, 1.0])).tolist())  # [3.0, 3.0]
print((A @ np.array([1.0, -1.0])).tolist()) # [1.0, -1.0]
values, vectors = np.linalg.eig(A)
print(np.sort(np.round(values, 6)).tolist()) # [1.0, 3.0]
print(np.allclose(A @ vectors[:, 0], values[0] * vectors[:, 0])) # True
```

`np.linalg.eig()` returns eigenvalues and matching eigenvectors as *columns* of `vectors`. The order of the pairs is not a promise; a vector and its negative describe the same eigen-direction. Check each returned pair with the equation instead of hard-coding exact vector signs. Some other real matrices have complex eigenvalues or vectors; this small symmetric example stays real.

## Guided lab

Download [Linear-algebra array operations lab](QAI.02.02.27_Linear_Algebra_Array_Operations_Lab.zip), extract it, and run in the folder:

```bash
python -m pip install -r requirements.txt
python linear_algebra_array_operations.py
python check_linear_algebra_array_operations.py
```

The program traces a matrix-product cell, solves the system, and verifies every eigenpair. The checker tests shapes, values, the inverse identity, and singular-matrix failures; it prints `All checks passed.`

**Trace before running:** predict `A @ B` at `[0, 0]` as 5, but `A * B` at `[0, 0]` as 2. For `A @ x = [5, 4]`, substitute `x = [2, 1]` into each row.

**Controlled variation:** copy `b` and change it to `[6, 6]`. Solving with the same `A` gives `[2, 2]`; verify `A @ [2, 2] == [6, 6]`. The original `b` remains `[5, 4]`.

**Debug:** A shape mismatch such as `(2, 3) @ (2, 3)` fails because the inner lengths 3 and 2 disagree; inspect which columns represent inputs and which rows represent matching inputs before changing the layout. If an inverse or solve fails on `singular`, inspect rank and independent equations. If a computed eigenvector has opposite signs to an example, test `A @ q ≈ λq` rather than assuming the direction is wrong.

## Independent mini-project: two linked quantities

Use `C = np.array([[3.0, 1.0], [1.0, 3.0]])`, `D = np.array([[1.0, 0.0], [2.0, 1.0]])`, vectors `p = [2.0, 1.0]`, `q = [4.0, 3.0]`, and target `t = [7.0, 5.0]`. Compute element-wise and matrix products of `C` and `D`, dot and outer products of `p` and `q`, solve `C @ x = t`, and report determinant, rank, inverse, eigenvalues, and an eigenpair check. The lab contains `mini_project_reference.py`.

Expected output (rounded where shown):

```text
element-wise [[3.0, 0.0], [2.0, 3.0]]
matrix [[5.0, 1.0], [7.0, 3.0]]
dot 11.0
outer [[8.0, 6.0], [4.0, 3.0]]
solution [2.0, 1.0]
verified True
determinant 8.0 rank 2
inverse [[0.375, -0.125], [-0.125, 0.375]]
eigenvalues [2.0, 4.0]
eigenpair verified True
```

Full reference solution:

```python
import numpy as np

C = np.array([[3.0, 1.0], [1.0, 3.0]])
D = np.array([[1.0, 0.0], [2.0, 1.0]])
p = np.array([2.0, 1.0])
q = np.array([4.0, 3.0])
t = np.array([7.0, 5.0])
x = np.linalg.solve(C, t)
values, vectors = np.linalg.eig(C)
pair_ok = all(np.allclose(C @ vectors[:, i], values[i] * vectors[:, i])
              for i in range(len(values)))
print("element-wise", (C * D).tolist())
print("matrix", (C @ D).tolist())
print("dot", np.dot(p, q))
print("outer", np.outer(p, q).tolist())
print("solution", np.round(x, 6).tolist())
print("verified", bool(np.allclose(C @ x, t)))
print("determinant", round(float(np.linalg.det(C)), 6),
      "rank", np.linalg.matrix_rank(C))
print("inverse", np.round(np.linalg.inv(C), 3).tolist())
print("eigenvalues", np.sort(np.round(values, 6)).tolist())
print("eigenpair verified", pair_ok)
```

## Check your understanding

1. **Why is `A * B` different from `A @ B`?** `*` multiplies corresponding cells; `@` sums row-by-column products.
2. **What does `np.dot([2,1], [3,4])` give?** `2×3 + 1×4 = 10`.
3. **What is the useful check after `np.linalg.solve(A, b)`?** Multiply `A @ x` and compare it approximately with `b`.
4. **What does rank 1 mean for `[[1,2],[2,4]]`?** Its rows are dependent; it has no inverse or unique square-system solution.
5. **How do you verify an eigenpair?** Check `A @ q` is approximately `λ * q` for its returned eigenvalue and vector.

Remember: track shapes and row-by-column products, then verify numerical answers by substituting them into the defining equation.

## Further reading

- [NumPy: linear algebra](https://numpy.org/doc/stable/reference/routines.linalg.html)
- [NumPy: matmul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html), [dot](https://numpy.org/doc/stable/reference/generated/numpy.dot.html), [inner](https://numpy.org/doc/stable/reference/generated/numpy.inner.html), and [outer](https://numpy.org/doc/stable/reference/generated/numpy.outer.html)
- [NumPy: solve](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html), [matrix_rank](https://numpy.org/doc/stable/reference/generated/numpy.linalg.matrix_rank.html), and [eig](https://numpy.org/doc/stable/reference/generated/numpy.linalg.eig.html)
