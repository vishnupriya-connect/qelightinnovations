# QAI.01.31 — Configuration and secrets

> QAI.01.30 notebook workflow → **QAI.01.31 configuration and secrets** → QAI.01.32 Git fundamentals

## 1. Destination: change settings without changing code or exposing credentials

Your course assistant can run with a local example now and may later call a model provider. A setting such as the request timeout can live in a file that classmates share. A provider's API key gives access to an account and must not be placed in that shared file.

By the end you will run the [practice project](QAI.01.31_Config_Secrets_Lab.zip), change a timeout, switch a simulated mode using a **fake** credential, check ignored files, and write a response to a pretend key leak. There are no real service calls or paid accounts in this lesson.

**Mental model:** the program is the recipe; configuration chooses how it runs; a credential is permission to access something. Sharing the recipe and safe choices does not grant permission.

## 2. Configuration: ordinary choices the program reads

- **Configuration:** values that choose program behaviour without changing the program's instructions.
- **Configuration value:** one such value, for example a 15-second timeout.
- **Configuration file:** a stored collection of values, such as `config.json`.

Our file contains only non-secret values:

```json
{
  "mode": "demo",
  "model_name": "example-text-model",
  "request_timeout_seconds": 15
}
```

Here `mode` chooses a local demonstration or a simulated remote mode. `model_name` is an invented label for this lesson, not a provider model ID. `request_timeout_seconds` is a maximum wait setting, not a guarantee that a response will arrive. In this project, the loader validates values but makes **no request**.

| Value | Example | Where it belongs | Reason |
|---|---|---|---|
| Display name, timeout, allowed local mode | `example-text-model`, `15` | Shared `config.json` | Safe to review and version |
| Provider credential | Real API key | Approved secret store or locally provided process environment | Grants access to an account |
| Example name of a required variable | `DEMO_AI_API_KEY` | Shared `.env.example` or README | Names a slot; contains no real key |

Before using configuration, check its *shape*: mode must be one of the supported words; timeout must be a positive integer within the chosen range; model name must be nonempty text. Python accepts `True` as an `int` subclass, so the lab checks `type(value) is int` to reject `true` as a timeout. Reading valid JSON alone does not prove that its values are valid for the application.

### Run the first experiment

Unzip the project, open a terminal in its folder, and run `python config_loader.py` (or `python3 config_loader.py` if that is your Python command). Expected:

```text
Loaded mode: demo
Model label: example-text-model
Timeout seconds: 15
Credential supplied: no
```

Change the timeout in `config.json` from `15` to `20` and rerun. Only that output value should change. Restore `15` afterward. **Why:** the data file changes behaviour without editing loader logic.

## 3. Credentials and their forms

A **credential** is information used to prove identity or permission. It may identify a person, program, or service.

| Term | Meaning | Practical distinction |
|---|---|---|
| **Username** | Account identifier | Often public or discoverable; by itself usually does not grant access |
| **Password** | Private value checked during sign-in | A password plus account identity may grant access; do not paste into examples |
| **Token** | Issued access value with permissions and often an expiry | Treat as secret whenever possession grants access |
| **API key** | Key a program presents to an API | May authorise usage or billing; treat as secret |
| **Secret** | Any value whose disclosure permits misuse or reveals restricted information | A password, live token, and live API key qualify |

An **API** is a program interface through which one program asks another program to do something. Some APIs require a credential. A key is not a model, prompt, or answer; it is an access instrument. A value named `DEMO_AI_API_KEY` in our exercises is only an **invented string**. It works with no provider and cannot authorise a request.

**Rule:** do not put real credentials in source code, notebooks, screenshots, sample outputs, shared documents, Git repositories, prompts sent to another service, or debugging logs.

## 4. An environment variable supplies a local value

An **environment variable** is a named value supplied to a process when it runs. A process is a running program. Python can read it with `os.environ.get`:

```python
import os

key = os.environ.get("DEMO_AI_API_KEY")
if key is None:
    print("No credential was supplied")
else:
    print("Credential supplied")    # Do not print key.
```

This example checks presence only. Environment variables are a useful local interface; they are **not encryption** and can still leak through careless logs, child processes, runtime inspection, or exposed machines. For production, use your deployment platform's approved secret injection or secret manager with scoped permissions. Details of those systems come later.

**Missing and empty differ:** `os.environ.get("NAME")` returns `None` when the name is absent and `""` for an explicitly empty value. Our simulated remote mode rejects both. In demo mode a credential is unnecessary.

Use an invented value for the experiment:

```bash
DEMO_AI_API_KEY=LOCAL_TEST_ONLY_FAKE_KEY python config_loader.py
```

That command still says `demo` because `config.json` says `demo`. Do not type a *real* key into a shell command: a command line may enter history or be observed. The project README also gives a PowerShell version using **only fake text**.

### Change mode without touching the real settings file

The project supplies `remote_demo.json` with `"mode": "remote"`. It is *simulated*: no call to a provider occurs. Run:

```bash
python config_loader.py --config remote_demo.json
```

Expected: a controlled failure because no credential was supplied. Next run:

```bash
DEMO_AI_API_KEY=LOCAL_TEST_ONLY_FAKE_KEY python config_loader.py --config remote_demo.json
```

Expected: `Loaded mode: remote` and `Credential supplied: yes`. You should **never** see the fake key printed. The project's automated checks exercise these cases without requiring a shell.

## 5. `.env` and `.env.example` are different

A `.env` file is a local text file commonly used to record environment variable names and values for development. The leading dot does **not** make its contents secret. Also, Python does **not** load a `.env` file automatically. You would need a deliberate loader or another tool; this project directly reads the process environment and does not need `.env` to run.

- `.env.example`: shared *template* containing names and obvious placeholders; no real values.
- `.env`: possibly private local values; keep it off shared drives and out of version history, and restrict access to the machine.
- `.gitignore`: a file of patterns telling Git which **untracked** paths to leave out of new tracking.

The lab's `.env.example` contains only:

```text
# Example only; this file is not automatically loaded.
DEMO_AI_API_KEY=PASTE_YOUR_OWN_KEY_HERE
```

The lab's `.gitignore` contains `.env`, `.env.*` and an exception for `!.env.example`. The exception keeps the safe template shareable. A pattern that matches a filename is not a substitute for checking what you actually committed.

To check in an existing **local** Git repository: `git check-ignore -v .env` should show the matching rule, and `git ls-files -- .env` should produce no output. The first checks the ignore pattern; the second checks whether Git **already tracks** that path. A file tracked earlier stays tracked even after adding it to `.gitignore`. QAI.01.32 teaches Git in depth; the project README supplies the commands.

**Private repository:** access is limited to authorised people, but they can still receive files and see history. **Public repository:** anyone can read the published files and history. Neither status makes it acceptable to commit an active API key or password. Git's ignore rule does not erase history or copies someone already received.

## 6. Work through a simulated exposure

**Secret exposure** means a credential became accessible to someone or somewhere it should not have been. Examples: an API key printed into a shared notebook output, committed to a repository, posted in a screenshot, or sent to an unauthorised person.

Use *only this invented incident*: at 10:00 a developer accidentally puts the label `SIMULATED_KEY_A` into a practice commit. This label is not a working credential.

| Sequence | Real incident action | Safe simulation in this lesson |
|---|---|---|
| 1. Stop use | Identify affected account and disable/revoke exposed credential at its issuer as soon as possible | Mark `SIMULATED_KEY_A` as **revoked** in the response record |
| 2. Replace | Create a new, scoped credential; deliver it securely to intended runtime; check the app works | Mark `SIMULATED_KEY_B` as the **replacement**; no real issuance |
| 3. Investigate | Assess time exposed, repository and fork visibility, logs, usage/billing, and people who could access it | Record public/private visibility and hypothetical reach |
| 4. Remove copies | Remove the credential from code, logs, and appropriate repository locations; coordinate history cleanup when needed | Replace the practice line with a placeholder; do not treat deletion as revocation |
| 5. Prevent repeat | Confirm ignored files, secret scanning, least privilege, usage limits, and owner for future rotation | Run the lab checks; document owner and a preventive change |

**Secret rotation** means replacing the old credential with a new one and disabling the old one. Removing text from the latest commit **alone** does not invalidate the old key and may leave it in history. For an actual leak, revoke/rotate first; follow the provider and incident-response process. Do not paste the exposed value into a new issue or incident report.

The project includes a **completed** `exposure_response_example.md` and a blank `exposure_response_template.md` that you can fill for the pretend event. The record should have a timestamp, scope, actions, verification, and follow-up. Never put real credential bytes in it.

## 7. Mini-project: the complete sequence

1. Unzip the practice project and read its `README.md`.
2. Run the demo with no credential and change `request_timeout_seconds` to 20; explain its effect.
3. Run the simulated remote mode with no credential; capture its generic error and exit code. Then provide the **fake** value and confirm successful loading with no key disclosure.
4. Run `python check_lab.py`; expect `Checks passed: 5`. Tests check valid demo, missing credential, fake credential without disclosure, bad timeout, and missing configuration.
5. Optional when Git is available: initialise **only this practice directory** as a local repository, run the ignore check, inspect which files would be staged. Do not connect a remote or push.
6. Read the completed exposure record. Make a new copy of the template and describe whether a public or private repository changes the investigation. In both cases the key would need revocation.
7. Teach the distinction between deleting a value from a file, adding `.gitignore`, and rotating a credential. Give one example where only rotation closes the risk.

**Independent modification with answer:** require an integer timeout of at most 30 seconds instead of 60. Find the loader's condition `value > 60`, change it to `value > 30`, then add a test for 31. Expected: 30 succeeds, 31 fails with a controlled error. This changes a safe configuration rule, not credential handling.

## 8. Debugging and operational decisions

| Observation | Likely cause | Fix or interpretation |
|---|---|---|
| `Configuration failed; check file fields and environment.` | File missing, invalid JSON/values, or missing key in simulated remote mode | Check chosen file and supported fields; confirm presence of fake value in local test |
| Your `.env` changes but Python sees no variable | `.env` is just text; this lab does not load it | Set the *process* environment for the local test or add a deliberate loader in a later project |
| `git check-ignore` matches but the key is in history | Ignore applies to untracked files, not old commits | Rotate first if real; investigate exposure; coordinate cleanup |
| A private repository contains a key | Access is limited but disclosure may still occur | Revoke/rotate and review access; remove it from the code path |
| Test output shows a credential value | Log or exception included it | Stop sharing output, revise logging to show only presence, rotate if real |
| A deployment needs a long-lived real key | A local `.env` or ad hoc export is hard to govern | Use approved secret delivery, narrow permissions, lifecycle and usage monitoring |

**Production choices to explain:** grant only the permissions needed (**least privilege**), set available usage or spending limits, have an owner for credential rotation, log request identifiers and status without logging secret values, and know who responds if a key leaks. This lab demonstrates the decision and evidence; cloud secret managers and identity policies are later units.

## Remember

- Configuration values decide behaviour; credentials grant access.
- A username identifies an account; a password, live token, or API key can be a secret.
- An environment variable is a process input, not an encrypted vault.
- `.env.example` may be shared with placeholders; `.env` containing real credentials must not be committed.
- `.gitignore` does not stop tracking a file already tracked or erase history.
- Public and private repositories both require credential care.
- Exposed credential: **revoke/rotate first**, investigate scope, remove copies, then prevent recurrence.

## Primary references

- [Python: `os.environ` and `getenv`](https://docs.python.org/3/library/os.html)
- [Git: ignore rules and already tracked files](https://git-scm.com/docs/gitignore)
- [GitHub: keep API credentials secure](https://docs.github.com/en/rest/authentication/keeping-your-api-credentials-secure)
- [GitHub: removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
