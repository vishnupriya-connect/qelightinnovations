# QAI.01.27 — Python Environments

> QAI.01.26 Packages and dependencies → **QAI.01.27 Python environments** → QAI.01.28 Files and text data

## 1. Destination: make the same project work in a fresh interpreter

In QAI.01.26, you declared `packaging==26.3` and ran a package demo. A dependency declaration helps only if you install it into the **Python interpreter that runs the project**. This lesson shows how to create a separate project environment, identify its interpreter, install the declared dependency there, record the installed state, and recreate the environment next to the old one to verify repeatability.

Your P1 evidence is the `qelight-package-lab` project from QAI.01.26 plus `env_check.py` and a short before/after setup record. A successful recreation requires the dependency to be obtainable on the learner's machine; record failures honestly rather than claiming a command ran when it did not.

## 2. Environment, system Python, project environment

An **environment** is the interpreter and its available installed packages and settings for a run. **System Python** here means a general interpreter installed or managed outside this project. A **project environment** is one selected for this project's dependencies.

If you install all training dependencies into one shared interpreter, two projects can need different package versions and interfere with each other. A **virtual environment** created with Python's `venv` has its own interpreter entry point and package installation location. It is built from a base Python but normally does **not** expose the base interpreter's third-party packages. The operating system itself and external services are **not** isolated by `venv`: do not mistake it for a container or security sandbox. [Python `venv` documentation](https://docs.python.org/3/library/venv.html).

**Mental model:** two project workspaces can share a base Python installation while selecting separate package sets:

```text
base Python
├── qelight-package-lab/.venv   → this project's installed packages
└── another-project/.venv       → that project's installed packages
```

The name `.venv` is conventional, not magical. The actual **interpreter path** is the executable you run, such as `.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on Bash/Zsh.

## 3. Create environment and check its interpreter path

From the root of `qelight-package-lab`, with `requirements.txt` and `qelight_course/` already present, **create an environment**:

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)"
.\.venv\Scripts\python.exe -m pip --version
```

**Bash/Zsh:**

```bash
python3 -m venv .venv
./.venv/bin/python -c 'import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)'
./.venv/bin/python -m pip --version
```

`sys.executable` reports the actual Python executable used by the running process. `sys.prefix` refers to the current virtual environment; `sys.base_prefix` refers to the base Python. A virtual-environment run should print `True` for their inequality. The path itself depends on your computer and folder; **do not copy a sample path as evidence**. [Python `venv`: environment detection](https://docs.python.org/3/library/venv.html#how-venvs-work).

If the check prints `False`, investigate which executable the command invoked. A shell prompt that visually shows `(.venv)` is a hint, but `sys.executable` and prefix checks are more reliable evidence.

## 4. Activate environment; activation is optional

**Activate environment** means adjusting the current shell's command search path so an unqualified `python` invokes the environment's Python. Activation is a convenience, not a prerequisite for using the full interpreter path. [Python `venv`: activation](https://docs.python.org/3/library/venv.html#how-venvs-work).

**Windows PowerShell** (after creating `.venv`):

```powershell
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)"
python -m pip --version
deactivate
```

**Bash/Zsh:**

```bash
source .venv/bin/activate
python -c 'import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)'
python -m pip --version
deactivate
```

`deactivate` leaves the current shell's activated environment and restores the prior command path. It does **not** delete `.venv` or uninstall its packages. After deactivation, an unqualified `python` may select a different interpreter; check rather than guess. The explicit `.venv` interpreter still works after deactivation.

If PowerShell blocks `Activate.ps1` under the machine's script policy, use the explicit `.\.venv\Scripts\python.exe` commands from this lesson. A global security-policy change is unnecessary for the project exercise.

## 5. Install dependency into the chosen environment

**Install dependency** into the chosen project interpreter from the requirements file made in QAI.01.26:

```text
# requirements.txt at the project root
packaging==26.3
```

**Windows PowerShell, no activation needed:**

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip show packaging
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m qelight_course.demo
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**Bash/Zsh, no activation needed:**

```bash
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pip show packaging
./.venv/bin/python -m pip check
./.venv/bin/python -m qelight_course.demo
./.venv/bin/python -m unittest discover -s tests -v
```

Run these from the **project root**, so the requirements file and local `qelight_course` package are in their expected locations. `pip show packaging` must report the selected installed version; `pip check` checks declared package requirements; the demo and unit tests check project behaviour. If installation is unavailable due to network/package-source limits, stop at that point and record it; do not “repair” the situation by silently using a global package installation.

**Diagnose a common mismatch:**

```text
One Python says: packaging is installed
Project Python says: ModuleNotFoundError: No module named 'packaging'
Meaning: the installation and the execution likely used different interpreters.
Check: invoke both pip and the project with the same .venv Python path.
```

## 6. Small environment-inspection program

Create `env_check.py` at the project root. This file reports **runtime evidence** without exposing a private project path in a shared screenshot unless that path is appropriate to share:

```python
# env_check.py
import importlib.metadata
import sys

print("Python version:", sys.version.split()[0])
print("Interpreter path:", sys.executable)
print("Virtual environment:", sys.prefix != sys.base_prefix)

try:
    installed_version = importlib.metadata.version("packaging")
except importlib.metadata.PackageNotFoundError:
    installed_version = "NOT INSTALLED"
print("Packaging version:", installed_version)

if sys.prefix == sys.base_prefix:
    raise SystemExit("Wrong interpreter: expected a project environment")
if installed_version != "26.3":
    raise SystemExit("Dependency mismatch: expected packaging 26.3")
print("Environment check: PASS")
```

Run using `.\.venv\Scripts\python.exe .\env_check.py` in PowerShell or `./.venv/bin/python env_check.py` in Bash/Zsh. The first two printed values vary by machine. **Expected success criteria:** `Virtual environment: True`, `Packaging version: 26.3`, and `Environment check: PASS`.

**Controlled failures:** run `env_check.py` with the base interpreter and observe the “Wrong interpreter” category if it is not a virtual environment. Run with a fresh project virtual environment *before installing* the requirement: it should report `NOT INSTALLED` and then the dependency mismatch. These are **diagnostic outcomes**, not reasons to ignore the missing package.

This script compares installed distribution metadata rather than assuming that `import packaging` implies the correct distribution version. A successful check does not prove all imports, tests, or external calls work; run the project test command too.

## 7. Export dependency list: distinguish declaration from snapshot

**Export dependency list** means record what an environment currently has installed. From the project root:

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m pip freeze > environment-snapshot.txt
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip --version
```

**Bash/Zsh:**

```bash
./.venv/bin/python -m pip freeze > environment-snapshot.txt
./.venv/bin/python --version
./.venv/bin/python -m pip --version
```

`requirements.txt` is the **intentional project requirement** you decided to declare; `environment-snapshot.txt` is a **report of installed distributions** in that environment. Do not automatically replace the declared requirements file with a snapshot from a polluted shared environment. `pip freeze` reports the installed state; it does not perform dependency resolution or compute a lock file. [pip freeze reference](https://pip.pypa.io/en/stable/cli/pip_freeze/).

For the simple clean exercise, the snapshot should include a `packaging==26.3` line; other lines depend on Python/pip and what else was installed. Compare the recorded versions with what the project expects. Record the actual Python version separately: a requirements file alone does not install that interpreter.

## 8. Recreate environment next to the existing one

To **recreate environment** without deleting your working one, make a second disposable environment in the same project folder. Reinstall from the **declared** `requirements.txt` and rerun the checks.

**Windows PowerShell:**

```powershell
py -m venv .venv-rebuild
.\.venv-rebuild\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-rebuild\Scripts\python.exe .\env_check.py
.\.venv-rebuild\Scripts\python.exe -m pip check
.\.venv-rebuild\Scripts\python.exe -m qelight_course.demo
.\.venv-rebuild\Scripts\python.exe -m unittest discover -s tests -v
```

**Bash/Zsh:**

```bash
python3 -m venv .venv-rebuild
./.venv-rebuild/bin/python -m pip install -r requirements.txt
./.venv-rebuild/bin/python env_check.py
./.venv-rebuild/bin/python -m pip check
./.venv-rebuild/bin/python -m qelight_course.demo
./.venv-rebuild/bin/python -m unittest discover -s tests -v
```

**Evidence table to fill with actual values:**

| Check | `.venv` | `.venv-rebuild` |
|---|---|---|
| `sys.executable` | local path A | local path B |
| `sys.prefix != sys.base_prefix` | `True` | `True` |
| Python version | record actual | record actual |
| installed `packaging` version | 26.3 if install succeeded | 26.3 if rebuild succeeded |
| `pip check` | record actual | record actual |
| demo and unit tests | record actual | record actual |

Paths A and B **should differ** because the virtual environments are separate. The relevant versions and expected project behaviour should agree when using a compatible base Python and identical requirements. If they differ, investigate package availability, the Python interpreter, and what the file actually declares. A clean environment is recreated, not copied as a folder: virtual environments can contain machine-specific paths. [Python `venv` documentation](https://docs.python.org/3/library/venv.html).

## 9. Project hygiene and failure diagnosis

| Observation | Meaning to investigate | Concrete check |
|---|---|---|
| shell prompt shows `(.venv)` but app uses another Python | IDE/runner may select a different interpreter | run `sys.executable` in the actual app process |
| package appears under system Python only | wrong interpreter used for pip | run `.venv` Python's `-m pip show packaging` |
| `ModuleNotFoundError` in rebuilt env | requirement missing or install failed | inspect `requirements.txt`, pip output, environment path |
| `pip check` passes but test fails | dependency declarations compatible, behaviour still wrong | read failing test and traceback |
| one computer runs and another does not | Python/version/platform/package-source difference | compare setup record and interpreter paths |
| moved `.venv` fails despite files being present | environment paths can be location-specific | recreate it at new location |
| `pip freeze` has many unrelated packages | wrong or shared interpreter, or extra installs | reproduce a clean isolated environment |
| version update suddenly breaks demo | changed dependency without validating contract | restore tested pin, then review upgrade deliberately |

Keep project code, `requirements.txt`, and setup instructions in the project; keep generated `.venv` and `.venv-rebuild` directories **out of version control**. A basic `.gitignore` can include:

```text
.venv/
.venv-rebuild/
__pycache__/
```

These entries are project instructions for Git, not installation commands. Do not include credentials in the requirements file or setup record. Later reproducible-build and deployment work adds lock-file policy, CI, and container images.

## 10. Independent practical with complete solution

**Task:** You have an existing `qelight-package-lab` with `requirements.txt` containing `packaging==26.3`. A learner says “I installed it, but the import fails.” Show a complete investigation that finds the interpreter, creates a new environment `.venv-check`, installs the requirement, proves the installed version, runs the demo/tests, and records whether that new environment can reproduce the project. Provide both Windows PowerShell and Bash/Zsh commands.

**Windows PowerShell solution** (from project root):

```powershell
py -m venv .venv-check
.\.venv-check\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)"
.\.venv-check\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-check\Scripts\python.exe -m pip show packaging
.\.venv-check\Scripts\python.exe .\env_check.py
.\.venv-check\Scripts\python.exe -m pip check
.\.venv-check\Scripts\python.exe -m qelight_course.demo
.\.venv-check\Scripts\python.exe -m unittest discover -s tests -v
```

**Bash/Zsh solution** (from project root):

```bash
python3 -m venv .venv-check
./.venv-check/bin/python -c 'import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)'
./.venv-check/bin/python -m pip install -r requirements.txt
./.venv-check/bin/python -m pip show packaging
./.venv-check/bin/python env_check.py
./.venv-check/bin/python -m pip check
./.venv-check/bin/python -m qelight_course.demo
./.venv-check/bin/python -m unittest discover -s tests -v
```

**How to interpret results:** if `pip show` reports version 26.3 **in this interpreter**, `env_check.py` passes, and the project tests pass, the new environment can run the project. The original failed import likely used another interpreter or had an incomplete installation; confirm by comparing its `sys.executable` and pip output. If installation fails, record that exact failure rather than claim the import problem is fixed. Add `.venv-check/` to `.gitignore` if this is a retained disposable lab.

## 11. What to remember and retain

- An environment is the interpreter and its available packages; the system and project interpreters can differ.
- `venv` creates an isolated environment. `sys.executable` names the interpreter; `sys.prefix != sys.base_prefix` checks whether it runs inside a virtual environment.
- Activation changes shell command lookup; using the explicit interpreter path does not require activation; `deactivate` leaves an active shell environment without deleting it.
- Install requirements with that environment's `python -m pip`; check `pip show`, `pip check`, the demo, and project tests.
- `pip freeze` exports an installed-state snapshot, distinct from a reviewed project requirement and a lock file.
- Rebuild a disposable environment from project code and declared requirements; do not copy a `.venv` directory between locations.
- Retain `env_check.py`, `requirements.txt`, local test outputs, two-environment evidence table, and the failure investigation. A clean run on your machine is useful evidence, not a guarantee about every other deployment environment.

**Next:** QAI.01.28 teaches reading and writing files safely. QAI.01.29 applies it to CSV and JSON inputs that a future AI project may use.

---

**Node contract (S90):** `C | L3→L4 | H2–H3 | E3–E5 | A2–A4 | P1`. All eleven S86 environment items are covered with explicit cross-platform commands, runtime verification, requirements-based recreation, failure diagnosis, and a complete independent solution. Learner evidence is a locally executed setup and a recorded rebuild result; the text alone does not certify a live deployment.

## Reference documentation

- [Python `venv`: creation, activation, and recreation](https://docs.python.org/3/library/venv.html).
- [Python Packaging User Guide: pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).
- [pip: installed-package snapshots with `freeze`](https://pip.pypa.io/en/stable/cli/pip_freeze/).
- [pip: checking installed dependency compatibility](https://pip.pypa.io/en/stable/cli/pip_check/).
