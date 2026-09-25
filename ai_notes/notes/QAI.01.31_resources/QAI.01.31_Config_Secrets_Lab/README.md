# Configuration and secrets — local practice lab

This self-contained Python lab makes no network requests and uses no real credentials. Read the companion QAI.01.31 notes first. You need Python 3.9+ for these commands; Git is optional.

## 1. Run and change safe configuration

From this directory:

```text
python config_loader.py
python check_lab.py
```

On systems using `python3`, substitute that command. Expect `Loaded mode: demo` and `Checks passed: 5` respectively. Change the timeout in `config.json` from `15` to `20`, rerun, then restore `15`.

## 2. Use only an invented credential

`remote_demo.json` enables a **simulation**. With no process variable present, this must fail:

```text
python config_loader.py --config remote_demo.json
```

For Bash (Linux/macOS/WSL), run with the **invented**, nonworking string:

```bash
DEMO_AI_API_KEY=LOCAL_TEST_ONLY_FAKE_KEY python config_loader.py --config remote_demo.json
```

For PowerShell (Windows), run:

```powershell
$env:DEMO_AI_API_KEY = "LOCAL_TEST_ONLY_FAKE_KEY"
python config_loader.py --config remote_demo.json
Remove-Item Env:DEMO_AI_API_KEY
```

PowerShell leaves the value in that terminal's environment until you remove it. Both examples use a fake value, never an account key. For a real secret, do not type its bytes in commands, code, documentation, or shell history; follow the platform's credential injection method. `.env.example` names an optional variable but is not loaded automatically.

## 3. Check ignore behaviour (optional Git prelude)

Do this only in the unzipped practice folder, **not** in a project you already use:

```text
git init
git check-ignore -v .env
git ls-files -- .env
git status --short
```

The ignore check should name the matching rule; `git ls-files -- .env` should print nothing for this new practice repository. `.env.example` is not ignored. There is no need to create an actual `.env`, commit, link a remote, or push anything. Git details follow in QAI.01.32.

## 4. Simulate response to an exposure

Read `exposure_response_example.md`. Copy `exposure_response_template.md` and fill it for a hypothetical private repository instead of public. State who could have accessed the value, how you would disable it, what would be replaced, what you would check, and why ignoring a file afterward cannot erase exposure.

## 5. Evidence to keep

Keep your changed `config.json` result (safe values only), output of `python check_lab.py`, a written explanation of the different simulated mode outcomes, and your completed incident-response record. Do not share raw environment values.
