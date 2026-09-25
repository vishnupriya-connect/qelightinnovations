# QAI.01.26 — Packages and Dependencies

> QAI.01.25 Modules and imports → **QAI.01.26 Packages and dependencies** → QAI.01.27 Python environments

## 1. Destination: make a small project reproducible

The previous project imported your own `text_utils.py`. Larger programs import code distributed by others. To run such a project on another computer, you must know **what it depends on**, which versions you used, where those dependencies are installed, and how to check the resulting environment.

You will create a small `qelight_course/` import package and use one declared outside dependency to compare package-version strings. You will make an isolated environment, install a pinned requirement, run the project and its tests, and keep a short setup record. QAI.01.27 expands environment activation, recreation, and interpreter diagnosis.

## 2. Two meanings of “package”

An **import package** is a set of importable Python modules organised under a package name, often a directory with `__init__.py`:

```text
qelight_course/
├── __init__.py
├── labels.py
└── demo.py
```

Here `qelight_course` is the import package; `labels.py` is a module inside its **package directory**. You can write `from qelight_course.labels import ...`.

A **distribution package** is what a package manager such as **pip** installs into an environment. One distribution may supply one or more import packages, and its install name may differ from the import name. **Do not assume** that a successful `import name` tells you exactly which distribution to install or that importing your local directory has published it for others. Consult the project's distribution metadata and documentation when installing third-party code. [Python Packaging User Guide — distribution versus import package](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/).

## 3. Package manager, dependency, direct and transitive

A **package manager** installs, upgrades, and removes distributions; this lab uses pip via the chosen interpreter:

```text
python -m pip --version
python -m pip show packaging
```

`python -m pip` asks **that Python interpreter** to run pip. The `pip` executable found elsewhere on `PATH` might belong to a different Python, so tie the command to the interpreter deliberately.

A **dependency** is code that a project needs. A **direct dependency** is one that the project declares and uses. A **transitive dependency** is required by a direct dependency or another dependency:

```text
Your project  →  directly requires Distribution A
Distribution A  →  requires Distribution B
Your project  →  receives B transitively
```

The demo's direct third-party distribution is `packaging`. Our local `qelight_course` package imports it in `labels.py`. The dependency graph for some packages can be much larger than this simple picture; inspect installed metadata rather than guess the transitive set.

**Why it matters:** using a transitive distribution directly without declaring it makes your project fragile. An upstream package may stop depending on it, even if your code still imports it.

## 4. Package version, constraint, compatibility

A **package version** identifies a release, such as the **exercise's selected** `packaging==26.3`. A **version constraint** says which releases are allowed:

| Constraint example | Meaning | Practical consequence |
|---|---|---|
| `packaging==26.3` | exactly this release | stable version choice for this guided exercise, if available for your Python |
| `packaging>=26,<27` | a release at least 26 and below 27 | permits changes within that range |
| `packaging!=26.3` | any allowed release except this one | use only when a specific release is known unsuitable |

These are examples of Python packaging **version specifiers**. An exact pin chooses a distribution version; it does **not** guarantee that operating system, Python version, all transitives, platform-specific builds, or external services are the same. **Version compatibility** means the chosen versions and runtime can work together for the project's actual tasks; an installer finding a solution is not proof that every application behaviour is correct. [Python Packaging User Guide — version specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/).

For this teaching lab, version `26.3` is a tested version in the preparation environment. Before adapting the lab to a different date or Python runtime, verify that the release and compatibility fit that environment; record any deliberate version change. The core skill is specifying and testing a chosen version, not memorising today's number.

## 5. Package installation in a disposable project environment

Create the environment **inside a new project folder**. This stage uses its interpreter directly; QAI.01.27 teaches activation and full recreation. Avoid installing training dependencies into the system Python by accident. [Python Packaging User Guide — pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

**Windows PowerShell** (run in the project's root folder):

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip --version
.\.venv\Scripts\python.exe -m pip install "packaging==26.3"
.\.venv\Scripts\python.exe -m pip show packaging
```

**Bash/Zsh** (run in the project's root folder):

```bash
python3 -m venv .venv
./.venv/bin/python -m pip --version
./.venv/bin/python -m pip install 'packaging==26.3'
./.venv/bin/python -m pip show packaging
```

`venv` creates an isolated project interpreter. These commands **install** into that environment without requiring shell activation. Installation needs access to a suitable package source and can fail if unavailable; do not claim success until `pip show packaging` and the project run succeed. This is a **controlled lab**: it does not install into the machine's general Python when the `.venv` interpreter is used.

## 6. Requirements file: declare what to install

A **requirements file** is a pip-readable set of installation requirements. Place `requirements.txt` at the project root:

```text
packaging==26.3
```

Install from that file, from the root folder:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

```bash
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pip check
```

`-r` tells pip to read the file. `pip check` verifies that installed distributions declare compatible dependencies; it does **not** run your application or prove that its outputs are correct. Do both `pip check` and the tests. Pip requirements can contain more than simple distribution pins; keep this beginner file simple. [pip requirements-file reference](https://pip.pypa.io/en/stable/reference/requirements-file-format/) · [pip check reference](https://pip.pypa.io/en/stable/cli/pip_check/).

**Record versions:** run the project's `python --version`, `python -m pip --version`, and `python -m pip show packaging` (using the actual `.venv` interpreter path). Record the results with the code commit or training notes. A `requirements.txt` with only direct dependencies does not necessarily fix every transitive version.

## 7. Guided P1 mini-project: import package plus one dependency

From the project root, create:

```text
qelight-package-lab/
├── requirements.txt
├── qelight_course/
│   ├── __init__.py
│   ├── labels.py
│   └── demo.py
└── tests/
    └── test_labels.py
```

### `qelight_course/__init__.py`

Create an empty file. Its presence marks this directory as a regular import package; it does not need demo code. The package name, `qelight_course`, is the name you import from project-root runs.

### `qelight_course/labels.py`

```python
# qelight_course/labels.py
from packaging.version import Version


def format_lesson(code, title):
    """Return one display label using provided code and title."""
    return f"{code}: {title.strip()}"


def supports_version(installed, minimum):
    """Compare two valid Python package-version strings."""
    return Version(installed) >= Version(minimum)
```

`from packaging.version import Version` is this project's direct third-party import. The exact text of `installed` is **supplied to the function**; the function compares version strings and does not inspect the machine's installed package version. Invalid version strings raise an error; validation/error policy for arbitrary input was introduced in QAI.01.23.

### `qelight_course/demo.py`

```python
# qelight_course/demo.py
from qelight_course.labels import format_lesson, supports_version


def main():
    print(format_lesson("QAI.01.26", " Packages "))
    print("Meets example minimum:", supports_version("26.3", "26.0"))
    print("Below example minimum:", supports_version("25.0", "26.0"))


if __name__ == "__main__":
    main()
```

`python -m qelight_course.demo` runs the module by its **package-qualified name** from the project root. The package has to be resolvable from that root, and the current environment must have the declared third-party dependency installed.

### `tests/test_labels.py`

```python
# tests/test_labels.py
import unittest
from qelight_course.labels import format_lesson, supports_version


class LabelTests(unittest.TestCase):
    def test_formatting(self):
        self.assertEqual(format_lesson("QAI.01.26", " Packages "),
                         "QAI.01.26: Packages")

    def test_equal_version_meets_minimum(self):
        self.assertTrue(supports_version("26.3", "26.3"))

    def test_older_version_does_not(self):
        self.assertFalse(supports_version("25.0", "26.0"))


if __name__ == "__main__":
    unittest.main()
```

### Run from the project root

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m qelight_course.demo
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

**Bash/Zsh:**

```bash
./.venv/bin/python -m qelight_course.demo
./.venv/bin/python -m unittest discover -s tests -v
./.venv/bin/python -m pip check
```

**Expected demo output:**

```text
QAI.01.26: Packages
Meets example minimum: True
Below example minimum: False
```

The tests should report **3 tests, OK**. `pip check` should report no broken package requirements in a successful compatible environment; the exact text and installed baseline packages can vary. Keep the recorded actual environment details instead of copying a fabricated installation log.

## 8. Package upgrade and removal: deliberate operations

A **package upgrade** changes an installed distribution to another allowed version. A **package removal** uninstalls it. Only use the project's interpreter:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade packaging
.\.venv\Scripts\python.exe -m pip uninstall packaging
```

```bash
./.venv/bin/python -m pip install --upgrade packaging
./.venv/bin/python -m pip uninstall packaging
```

These are **syntax demonstrations**: do not run the upgrade as a routine part of the lab, because it may change what the pin in `requirements.txt` promised. If you intentionally test removal, the demo import should fail with `ModuleNotFoundError`; reinstall with `-r requirements.txt` and rerun the tests. Before a real upgrade, choose a target version, review the change, test in a disposable environment, and update the recorded dependency decision.

## 9. Lock file: distinct from a simple requirements list

A **lock file** records a resolved set of exact package versions (and, depending on the format/tool, additional source or integrity details) for repeatable installation. It differs from a requirements file listing only your direct dependency, such as `packaging==26.3`: that line does not by itself fix every transitive dependency.

`pip freeze` reports installed distributions and their versions; its output can be useful as an **environment snapshot**, but the pip docs distinguish it from computing a lock file or solver result. Modern tooling includes a `pylock.toml` interoperability specification; the exact generation and installation workflow depends on the selected tool. Learn lock-file generation and review within the later project workflow; do not invent a lock file by renaming a requirements file. [pip freeze reference](https://pip.pypa.io/en/stable/cli/pip_freeze/) · [Python Packaging User Guide — pylock.toml specification](https://packaging.python.org/en/latest/specifications/pylock-toml/).

## 10. Dependency conflict: incompatible requirements

A **dependency conflict** occurs when the chosen requirements cannot all be met. For example, requiring **both** `packaging==26.3` and `packaging<26` is logically impossible: no version can be both 26.3 and below 26. Such contradictory lines belong in a **disposable thought experiment**, never in the actual lab requirements.

Real conflicts can involve transitives or a Python-version constraint, and an installer may report that no compatible solution exists. Diagnose by:

1. reading the exact conflicting requirements and target Python version;
2. locating which project or distribution requires each bound;
3. deciding which declared constraint can safely change;
4. applying the change to a disposable environment and rerunning `pip check` plus application tests.

Do not force a broken environment to appear successful with `--no-deps` or a blind upgrade. A passed installer run alone does not establish behavioural compatibility; the demo and tests remain necessary. [pip dependency resolution](https://pip.pypa.io/en/stable/topics/dependency-resolution/).

## 11. Debug common packaging mistakes

| Symptom | Likely cause | Check |
|---|---|---|
| `ModuleNotFoundError: No module named 'packaging'` | dependency absent from the active interpreter | use the project's interpreter with `-m pip show packaging` |
| `ModuleNotFoundError: No module named 'qelight_course'` | run from wrong location or package folder missing | from project root use `-m qelight_course.demo`; check `__init__.py` |
| `pip show packaging` succeeds but project import fails | pip and Python may be different interpreters | compare the exact interpreter prefix on both commands |
| requirement installs but test fails | compatibility or logic is not proved by installation | inspect failing test and installed version |
| `{}` is called an “empty package” | dictionary syntax confused with package concept | a package here is a directory/module structure or installed distribution |
| `pip freeze` contains unrelated packages | snapshot taken from a shared/global interpreter | recreate a clean project environment and record its interpreter |
| solver reports incompatible constraints | requested versions cannot coexist | find who declared each bound before changing it |
| direct `python qelight_course/demo.py` cannot import package | execution path is inside the package, not its parent | run `python -m qelight_course.demo` from the project root |

**Debug record:** write the project root, Python path, pip path, relevant `pip show` result, requirement line, exact command, actual error type, root cause, fix, and a rerun result. Do not paste credentials or private repository URLs into shared setup notes.

## 12. Independent task with complete solution

**Task:** create a second module `qelight_course/levels.py` with `at_least(installed, required)` using `packaging.version.Version`. It must return `True` for equal versions, `False` for an older version, and `True` for a newer version. Add a standard-library unit test file under `tests/`. State the dependency declaration and exact commands to run.

**Solution for `qelight_course/levels.py`:**

```python
from packaging.version import Version


def at_least(installed, required):
    """Compare two valid package-version strings."""
    return Version(installed) >= Version(required)
```

**Solution for `tests/test_levels.py`:**

```python
import unittest
from qelight_course.levels import at_least


class VersionLevelTests(unittest.TestCase):
    def test_equal(self):
        self.assertTrue(at_least("26.3", "26.3"))

    def test_older(self):
        self.assertFalse(at_least("25.9", "26.0"))

    def test_newer(self):
        self.assertTrue(at_least("26.3", "26.0"))


if __name__ == "__main__":
    unittest.main()
```

The existing `requirements.txt` remains `packaging==26.3`. From the project root, run the same environment's `python -m pip install -r requirements.txt`, then `python -m unittest discover -s tests -v`. With both test files present, expect **6 tests, OK**. The version strings in this exercise are fictional comparisons supplied to the function; they do not query the installed release.

## 13. What to remember and retain

- An import **package** (modules in a directory) and an installed **distribution package** are related but distinct.
- pip manages distributions; bind it to the intended Python interpreter with `python -m pip`.
- Declare direct dependencies; transitive dependencies come through the declared packages.
- A version specifier chooses allowed releases; an installed version still needs runtime and behaviour checks.
- Install from a simple requirements file in an isolated environment; check installed metadata, `pip check`, and project tests.
- Upgrade and removal are deliberate changes in that environment, not blind fixes for import errors.
- A lock file represents a resolved dependency set; `pip freeze` is an installed-state snapshot.
- Retain the `qelight-package-lab` tree, requirement line, commands, actual version evidence, 3-test/6-test outputs, and one failure/recovery record. Record whether the packaging release is available in the student's target environment before adopting this particular pin there.

**Next:** QAI.01.27 makes the project interpreter, activation, exported snapshot, and clean recreation procedure fully explicit.

---

**Node contract (S90):** `C | L3→L4 | H2–H3 | E3–E5 | A2–A4 | P1`. All fifteen S86 package/dependency items are covered through an isolated package mini-project, a declared dependency, executable tests, conflict diagnosis, and a solved independent extension. Environment recreation and deeper lock-file policy continue in QAI.01.27 and later operations work.

## Reference documentation

- [Python Packaging User Guide: installing with pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).
- [Python Packaging User Guide: distribution versus import packages](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/).
- [pip: requirements file format](https://pip.pypa.io/en/stable/reference/requirements-file-format/).
- [pip: freeze, check, and dependency resolution](https://pip.pypa.io/en/stable/).
