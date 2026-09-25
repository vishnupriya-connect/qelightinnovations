# QAI.01.32 — Git fundamentals

> QAI.01.31 configuration and secrets → **QAI.01.32 Git fundamentals** → QAI.02 relational and tabular data

## 1. Destination: keep a traceable, shareable course project

Our small course app reads `lessons.json` and prints a list of topics. You will change it in stages, record why each change exists, practise a conflict, and sync two local copies. The companion [practice project](QAI.01.32_Git_Lab.zip) includes starter files and a worked history you can inspect. The local remote exercise needs **no website or account**.

**Version control** records changes to files over time, so you can answer: *what changed, who recorded it, and why?* **Git** is a version-control tool. A **repository** is a project together with Git's recorded history and internal bookkeeping. The hidden `.git` directory holds that bookkeeping; a plain folder of files without it is not yet a Git repository.

You should be able to run the app, explain the difference among working, staged, and committed versions, and recover your bearings when a merge cannot be completed automatically.

## 2. Four places your work can exist

| Place | Meaning | Lab example |
|---|---|---|
| **Working tree** | Files currently visible in your project folder | The `WELCOME_TEXT` line you edited in `notes_app.py` |
| **Staging area** (index) | The exact version of selected changes to include in the *next* commit | Changes selected by `git add notes_app.py` |
| **Local repository** | Commits recorded on this machine | `git log` shows the lesson-app history |
| **Remote repository** | Another repository Git knows by a name and **remote URL** | `origin` points to the lab's separate bare repository |

A **tracked file** is already known to Git. A newly created file is **untracked** until added. An **ignored file** matches a rule in `.gitignore`, such as `.env` or `__pycache__/`, so Git normally leaves it untracked. An ignored file that was tracked earlier does *not* disappear from history. Before publishing, inspect both your staged diff and committed history for secrets.

**Mental model:** working tree = current desk; staging = the chosen items in a packing box; commit = a labelled sealed snapshot; remote = another repository that can receive snapshots. A command that edits your desk is not the same as one that seals or sends the box.

### Create a local repository deliberately

Unzip the lab. Open a terminal inside its `QAI.01.32_Git_Lab` folder and run:

```text
python notes_app.py
git init -b main
git config user.name "QElight Learner"
git config user.email "learner@example.invalid"
git status --short
```

Use `python3` if that is your Python command. Configure identity **for this lab only**. The `.invalid` address is an invented placeholder; no email is sent. `git init -b main` creates a **main branch** called `main`. A **branch** is a named pointer to a line of commits; `main` is simply the conventional primary branch name for this lab.

**Expected:** `git status --short` shows starter files as `??` (untracked), except ignored files. Your computer's Git version may format status differently; read the filenames and their states.

## 3. Status and diff before a commit

`git status` reports changes relative to the staging area and last commit. `git diff` shows unstaged edits to tracked files; `git diff --staged` shows what is currently staged for the next commit. A **diff** describes changed lines: lines beginning with `-` were removed, `+` were added in the compared versions. For a brand-new untracked file, ordinary `git diff` does not show its contents until you stage it or use other inspection.

Make the first small commit:

```text
git add .gitignore README.md notes_app.py lessons.json
git diff --staged
git commit -m "Add course topic viewer and run instructions"
git status --short
```

Before committing, read the staged diff. `check_app.py` is still untracked because we selected four filenames, not everything. A **commit** records the staged versions of files plus metadata. A **commit message** briefly explains the purpose. `git log --oneline` shows **commit history** with shortened **commit identifiers**. A commit identifier is derived from the commit content and metadata; your exact identifier will differ from another learner's. It is not a sequential number.

Now create the second purposeful commit:

```text
git add check_app.py
git diff --staged
git commit -m "Add checks for lesson data and viewer output"
python check_app.py
git log --oneline
```

Expected: `Checks passed: 3` and two commits. At this stage you can run and validate the program from a fresh clone after you later publish to the local remote.

### Demonstrate that staging is a snapshot

After staging a change, editing the same file again makes its working version differ from the staged version. `git diff` shows the *new, unstaged* edits; `git diff --staged` still shows the previously staged content. Run `git add <filename>` again if you want the latest edit in the commit. Never assume `git add` means “always include future edits.” Do this only on a lab file; recheck `git status` before you commit.

## 4. Branch, switch, and create a controlled conflict

**Branch creation** makes a new line of work starting at a commit; **branch switch** changes which line your working tree represents. Always commit or deliberately manage uncommitted changes before switching. In this lab, both branches edit the **same line** differently, so Git will ask you to decide the final text.

Starting after the two commits above:

1. Run `git switch -c welcome-copy`. This creates and switches to the feature branch.
2. In `notes_app.py`, change exactly `WELCOME_TEXT = "AI study planner"` to `WELCOME_TEXT = "Your course learning guide"`. Save.
3. Run `git diff`, `python check_app.py`, `git add notes_app.py`, `git diff --staged`, then `git commit -m "Make course welcome text student friendly"`.
4. Run `git switch main`.
5. In `notes_app.py`, change its original line to `WELCOME_TEXT = "QElight course learning guide"`. Save.
6. Run `python check_app.py`, `git add notes_app.py`, `git commit -m "Identify QElight in course welcome text"`.
7. Run `git merge welcome-copy`. Expect a **merge conflict** in `notes_app.py`; Git cannot decide which replacement of the same line is right.

**Merge** combines another branch's work into the current branch. A conflict is a request for a human decision, **not** evidence that Git has lost all work. Stop and inspect `git status` and the file; do not use a force option.

Git puts markers around the disputed text. The exact marker label may vary:

```python
<<<<<<< HEAD
WELCOME_TEXT = "QElight course learning guide"
=======
WELCOME_TEXT = "Your course learning guide"
>>>>>>> welcome-copy
```

`HEAD` is your currently checked-out branch position. Between `<<<<<<<` and `=======` is the current branch's text; between `=======` and `>>>>>>>` is the incoming branch's text. Neither line automatically wins. Resolve by replacing the *whole marker block* with:

```python
WELCOME_TEXT = "QElight AI course learning guide"
```

Keep the rest of `notes_app.py` intact. Then:

```text
python check_app.py
git add notes_app.py
git diff --staged
git commit -m "Merge welcome copy with QElight wording"
git log --oneline --graph --all
git status --short
```

The `git diff --staged` view after conflict resolution may be less helpful than `git diff --check` and the file itself because merge stages have multiple versions. Check that no `<<<<<<<`, `=======` or `>>>>>>>` conflict markers remain and the program runs. The final status should be clean. The graph shows the two lines of history joined by a merge commit.

**If something unexpected happens:** `git merge --abort` *before committing a merge* attempts to return to the pre-merge state. Inspect status and do not use it on work you have not saved. Alternatively finish the conflict resolution shown above.

## 5. Clone, fetch, pull, and push without a hosting account

A **remote URL** is the address Git uses for another repository. It can be an HTTPS/SSH address on a server *or a local directory path*. In this exercise `origin` is a friendly remote name for a **local bare repository**. Bare means it holds Git history but has no checked-out working files.

From the first lab folder, after finishing the merge:

```text
git init --bare ../qai0132-remote.git
git -C ../qai0132-remote.git symbolic-ref HEAD refs/heads/main
git remote add origin ../qai0132-remote.git
git remote -v
git push -u origin main
git clone ../qai0132-remote.git ../qai0132-second-copy
git -C ../qai0132-second-copy log --oneline --graph --all
git -C ../qai0132-second-copy config user.name "QElight Learner"
git -C ../qai0132-second-copy config user.email "learner@example.invalid"
```

`push` sends local commits to a remote branch. `clone` creates another local repository with the files and reachable history; its new `origin` points to the bare repository. `git remote -v` prints the configured fetch/push destinations; here they are local paths. The `symbolic-ref` step lets new clones check out `main` by default.

In the **second copy**, open its `README.md` and add one line near the end: `Second copy verified: python check_app.py`. Save and from your **first folder** run:

```text
git -C ../qai0132-second-copy add README.md
git -C ../qai0132-second-copy commit -m "Document checks in second copy"
git -C ../qai0132-second-copy push origin main
git fetch origin
git log --oneline main..origin/main
git diff main..origin/main -- README.md
git pull --ff-only origin main
python check_app.py
git status --short
```

`fetch` downloads new commits and updates your **remote-tracking** reference `origin/main`; it does not change your working files on `main`. `git log main..origin/main` shows commits the remote has and local `main` lacks. `pull` fetches and integrates changes into the current branch; `--ff-only` allows this example's safe straight-line update and refuses if the two sides diverged. If refused, inspect both histories and agree on a merge/rebase path with the team; do not force-push. After successful pull, the README line appears in the first folder.

**Important:** the worked-history bundle in the zip is for inspecting a finished example. If you clone the bundle instead of following the steps, you will *not* recreate the learning sequence yourself; inspect it after your own attempt.

## 6. Pull request and code review

A **pull request** is a proposal on a hosting service to integrate one branch into another. The name does not mean it runs `git pull` on your laptop. A **code review** is another person's inspection of the proposed changes, tests, assumptions, security, and maintainability before accepting them.

For a real shared course project, you would push a feature branch to an authorised host, open a pull request targeting `main`, include how to run `python check_app.py` and screenshots/output when relevant, request review, address comments, then merge under the team's rules. This local lab has no hosted service, so **no actual pull request or external review is performed**. Practise a self-review: inspect `git diff main..welcome-copy` before merge and state what changed, what could fail, and what evidence you ran. Team release policies and CI/CD are covered later.

## 7. Troubleshoot by identifying which place is wrong

| Symptom | Check | Likely correction |
|---|---|---|
| Edited file missing from commit | `git status`, `git diff`, `git diff --staged` | Stage intended version, inspect staged diff, commit |
| `git diff` empty but file is new | `git status --short` shows `??` | `git add` that file, then inspect staged diff |
| Feature text disappeared after switching | `git switch -` and `git log --all` | Find it on the committed feature branch; do not assume uncommitted changes survive safely |
| `git merge` reports conflict | `git status` and conflicted file | Edit markers into one correct version; test, add, commit |
| `git push` rejected because remote advanced | `git fetch`; compare `main` and `origin/main` | Integrate reviewed changes; do not force-push |
| A secret appears in the staged diff | Stop before commit | Remove secret from the staged change; if already shared, follow QAI.01.31 rotation |
| README's run command fails in a clean clone | Read environment and relative paths | Fix instructions and project files, verify in a fresh clone |

The production habit is simple: check status; inspect exact differences; run the relevant test; keep commits purposeful; keep keys out; review shared changes before merging. Git makes the history inspectable, but the team still owns correctness and access decisions.

## 8. Small assessment with answers

1. **You changed `notes_app.py`, ran `git add notes_app.py`, changed it again, then committed. Which version was recorded?** The staged version from the time of `git add`, unless you staged again. Inspect `git diff` (latest unstaged changes) and `git diff --staged` (commit candidate).
2. **After `git fetch origin`, why does your README still show the old line?** Fetch updated `origin/main`; it did not integrate those commits into local `main`. Inspect and run the shown `git pull --ff-only origin main` when appropriate.
3. **Why can both branches pass `python check_app.py` while the merge conflicts?** Tests assess program behaviour; Git sees competing edits to the same source lines. A human must choose and test the merged text.
4. **Does a private remote make it safe to commit an API key?** No. Authorised viewers and copies can still see it; if exposed, rotate as taught in QAI.01.31.
5. **Does a pull request replace `git pull`?** No. A pull request proposes review and integration on a host; `git pull` synchronises and integrates into a local branch.

## Remember

- Working tree → stage selected content → commit locally → push when sharing.
- `git status` tells where files stand; `git diff` and `git diff --staged` show two different comparisons.
- A branch points to commits; a merge combines lines of work; a conflict needs an explicit human resolution.
- Fetch downloads and updates remote-tracking references; pull also integrates; push uploads; clone creates another copy.
- Inspect staged content and history before sharing; review changes and run the app from a clean clone.

## Primary references

- [Git: getting started and recording changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
- [Git: branches and merging](https://git-scm.com/docs/git-merge)
- [Git: working with remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)
- [Git: `gitignore`](https://git-scm.com/docs/gitignore)
