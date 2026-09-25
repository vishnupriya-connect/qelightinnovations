# QAI.01.32 — Git lab starter

This project reads fictional course topic records. It uses Python's standard library and Git locally; it needs no API account, internet connection, or secret.

## Run

From this folder:

```text
python notes_app.py
python check_app.py
```

Use `python3` where that is your Python command. Expect:

```text
AI study planner
Topics available: 2
QAI.01.31: Configuration and secrets
QAI.01.32: Git fundamentals
```

The checks should finish with `Checks passed: 3`.

## Follow the complete lesson

Open the companion `QAI.01.32_Git_Fundamentals_Notes.md` alongside this project. The lesson gives the exact order for initialising Git, recording two starter commits, creating a feature branch, resolving a merge conflict, making a separate local bare remote, cloning it, fetching, pulling, and pushing.

The included `worked_history.bundle` is an optional finished example with a safe local history. Inspect it *after* completing the commands yourself:

```text
git clone worked_history.bundle ../qai0132-example-view
git -C ../qai0132-example-view log --oneline --graph --all
python ../qai0132-example-view/check_app.py
```

The example commit identifiers will be different from the ones you create.
