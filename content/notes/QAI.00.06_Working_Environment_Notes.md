# QAI.00.06 — Working Environment

> **Position in the QElight AI path**  
> `QAI.00.05 Learning, implementation, and evidence habits` → **`QAI.00.06 Working environment`** → `QAI.00.07 Responsible AI and verification`

## 1. Why a working environment matters

An AI project does not run “inside the model.” It runs in an environment made of a computer or cloud machine, software, accounts, files, permissions, and settings.

If the environment is unclear, learners often face problems such as:

- code runs on one machine but not another;
- a notebook cannot find its data file;
- a package/version is missing;
- a service access key is exposed or does not work;
- a cloud bill grows unexpectedly;
- results cannot be repeated.

The goal here is not to memorise every tool. It is to understand the parts and work safely.

## 2. Working-environment map

```text
Your work environment
├─ machine
│  ├─ local computer
│  └─ cloud machine
├─ operating system
├─ browser
├─ editor / notebook environment
├─ files, code, data, and packages
├─ account and permissions
└─ credentials and secrets
```

## 3. Computer

- **Computer:** a machine that accepts input, processes instructions, stores information, and produces output.
- For AI work, a computer may be your laptop, desktop, remote server, or cloud machine.

### Important practical parts

| Part | Simple role in AI work |
|---|---|
| CPU | general processing; runs programs and many ordinary tasks |
| RAM / memory | holds currently running programs and data temporarily |
| storage | keeps files, code, notebooks, data, and models for later use |
| GPU | specialised processor useful for many deep-learning/image workloads |
| network connection | communicates with cloud services, APIs, data sources, and repositories |

You do not need an expensive machine to start Python, data work, API-based GenAI, or small projects. Larger deep-learning/fine-tuning/image-generation work may need a suitable GPU or cloud resource later.

## 4. Operating system

- **Operating system (OS):** core software that manages hardware, files, running programs, users, and permissions.
- Common operating systems: Windows, macOS, and Linux.

The OS is the layer between your programs and the physical machine.

```text
Your notebook / Python program
          ↓
Operating system
          ↓
Computer hardware
```

The same Python project can usually run on different operating systems, but installation commands, file paths, permissions, and tool setup may differ.

## 5. Browser

- **Browser:** application used to access websites and web applications.
- Examples of browser-based AI work:
  - cloud notebooks;
  - model-provider consoles;
  - documentation;
  - Git repositories;
  - hosted applications;
  - browser interfaces for AI tools.

### Practical habit

Keep separate browser profiles or clear account awareness when possible. You should know which account is signed in before creating API keys, enabling paid services, uploading data, or changing cloud settings.

## 6. Terminal

- **Terminal:** text-based application used to give commands to the operating system.
- **Command:** a short instruction entered in the terminal.

Later, you will use the terminal to:

- move between folders;
- create environments;
- install packages;
- run Python scripts;
- use Git;
- inspect logs;
- start local applications.

For now, remember only this:

```text
Graphical interface: click buttons and windows.
Terminal: write commands.
Both can control the same computer and files.
```

The detailed terminal lesson comes in `QAI.01`.

## 7. Editor

- **Editor:** software used to create and change text/code files.
- A code editor usually helps with syntax colouring, suggestions, file navigation, search, debugging, and extensions.

### Editor is not the programming language

| Item | Role |
|---|---|
| Python | language used to write instructions |
| editor | place where you write/edit Python files |
| interpreter | program that reads and runs Python code |
| terminal | place where you can run commands, including Python commands |

An editor helps you write code. It does not make code correct automatically.

## 8. Notebook environment

- **Notebook environment:** a workspace that combines explanatory text, runnable code cells, output, charts, and images.
- **Cell:** one independently runnable block in a notebook.
- Common uses: learning, experimentation, data analysis, model trials, and teaching demonstrations.

### Notebook flow

```text
Markdown cell: explain goal
       ↓
Code cell: run small step
       ↓
Displayed output: inspect result
       ↓
Markdown cell: explain what the result means
```

### Important notebook habits

- run from top to bottom in a fresh session;
- do not assume an old output proves current code works;
- save the notebook with meaningful name/version;
- record data/model/configuration used for important results;
- move stable reusable code into scripts/packages later.

## 9. Local environment

- **Local environment:** software and files running on your own computer.

### Advantages

- direct control over files and setup;
- can work without continuous internet for many tasks;
- suitable for learning Python and small projects;
- sensitive data may remain on the local machine when handled securely.

### Limits

- your machine has limited CPU, RAM, storage, and GPU;
- setup problems are your responsibility;
- other people cannot automatically access your local work;
- updates and backups need attention.

## 10. Cloud environment

- **Cloud environment:** computing resources provided over the internet by a service provider.
- It may provide notebooks, storage, APIs, databases, GPUs, deployment services, and monitoring tools.

**Browser location versus execution location:** a browser window runs on your own laptop, but a notebook opened in that window may execute its code on a provider's remote machine. Check where the code runs and where uploaded files are stored. Seeing a familiar website on your local screen does not mean your data stayed local.

### Advantages

- access stronger compute/GPU when needed;
- easier sharing and deployment in many cases;
- managed services reduce some setup work;
- scale resources up/down when designed carefully.

### Limits and responsibilities

- requires account, network access, and permissions;
- may incur cost;
- data sharing/location and permissions require care;
- resources must be stopped/removed when no longer needed;
- provider settings and quotas can affect behaviour.

### Local versus cloud

| Question | Local environment | Cloud environment |
|---|---|---|
| where does code run? | your own machine | provider’s remote machine/service |
| cost | mostly your existing hardware/electricity | usage-based or subscription cost possible |
| setup | you install/manage more | provider may manage more |
| compute capacity | limited by your machine | can be larger, subject to cost/quota |
| data control | direct local control | must manage access, region, policy, sharing |
| starting point | small Python/notebook learning | hosted notebook, API, deployment, GPU work |

**Practical path:** begin with a local Python/notebook setup and a simple hosted notebook option. Use cloud resources deliberately when a project needs them.

## 11. Account

- **Account:** identity used to sign in to a service.
- An account may identify a person, organisation, application, or automated process.

### Account controls

- what services you can access;
- what data/resources you can see;
- what you can create, change, or delete;
- what charges may apply;
- what actions are logged under your identity.

### Safe habit

- use your own authorised account;
- enable multi-factor authentication where available (a second sign-in check in addition to a password);
- do not share login passwords;
- review active sessions and payment/project settings;
- separate personal experiments from organisation/client work when required.

## 12. Credential

- **Credential:** information or mechanism that proves an identity or grants access.
- Examples: password, one-time code, access token, API key, certificate, or signed-in session.

### Identity versus permission

| Term | Question answered |
|---|---|
| authentication | “Who or what is requesting access?” |
| authorisation | “What is this identity allowed to do?” |

You will use these ideas later for APIs, cloud systems, databases, agents, and production applications.

## 13. API key

- **API key:** a value presented by an application when requesting access to an application programming interface (API), an agreed way one program requests work from another. The model-provider keys we use as credentials must be treated as secrets; some other services also publish non-secret identifiers called keys, so check the provider's instructions for the exact value.
- It may be linked to usage limits, billing, and permissions.

### Example flow

```text
Your application
  + request to a model-provider API
  + authorised API key
        ↓
Provider verifies allowed access
        ↓
Provider returns response or access error
```

### Non-negotiable rules

- Never paste a real API key into chat, a public document, screenshot, video, notebook output, or Git repository.
- Never place a real key directly inside source code that will be shared.
- Never use another person’s key without explicit permission.
- Restrict, rotate, or revoke a key if you think it was exposed.
- Set spend/usage limits and review activity where the provider supports them.

## 14. Secret

- **Secret:** any confidential value that must not be exposed because it can grant access or reveal protected information.
- API keys are secrets. Passwords, database credentials, access tokens, private certificates, and some connection strings are also secrets.

### Secret is different from ordinary configuration

| Safe to share in source/config example | Must be protected |
|---|---|
| model name | API key |
| chunk size | password |
| application port | database credential |
| project display name | access token |
| public API URL | private connection string |

If you are unsure, treat a value as a secret until confirmed otherwise.

## 15. Environment variable

- **Environment variable:** a named setting available to a running program from its environment.
- It is often used to provide configuration or secrets without writing them directly into source code.

### Conceptual example

```text
Variable name: MODEL_PROVIDER_API_KEY
Variable value: [private value stored outside shared source code]

Program asks for: MODEL_PROVIDER_API_KEY
Environment supplies the private value at run time.
```

### Important limit

Environment variables reduce accidental exposure in shared code, but they are not magical protection. The computer, cloud service, logs, permissions, and deployment configuration must still be secured.

## 16. One safe environment pattern for later GenAI projects

```text
Project folder
├─ notebook or script
├─ documented package requirements
├─ sample/non-sensitive data
├─ README with setup steps
├─ configuration template with placeholder values
└─ secrets stored outside shared project files
```

### Configuration template example

```text
MODEL_NAME=chosen-model-name
RETRIEVAL_TOP_K=4
MODEL_PROVIDER_API_KEY=REPLACE_WITH_PRIVATE_VALUE_IN_YOUR_OWN_ENVIRONMENT
```

This template may be shared. The file containing a real key must not be shared or committed to version control.

**Version control** means keeping a recorded history of changes to project files. Detailed setup comes later. A placeholder tells the reader what setting is needed; it must never contain a working credential.

## 17. Practical setup thought process

Before starting any AI notebook, API demo, or cloud project, ask:

1. Where will this run: local machine or cloud?
2. Which account is being used, and is it authorised for this work?
3. What data will be accessed or uploaded?
4. Are there costs, quotas, or usage limits?
5. Which settings are ordinary configuration?
6. Which values are secrets?
7. Where will the code, data, configuration, and outputs be saved?
8. Can this run be reproduced later?

### 17.1 Guided inspection — identify your actual working environment

This inspection requires only normal operating-system and browser screens. Do not copy passwords, active key values, recovery codes, private file paths, or account identifiers into the record you share.

1. Open your computer's ordinary **About/System information** screen. Record the operating system name; record only the resources relevant to the exercise, such as whether a local Python runtime is already available. You do not need to install anything yet.
2. Open the **browser** you use for course material. Decide whether the page is merely showing instructions, running an application remotely, or hosting a notebook whose code runs remotely. If you cannot tell, record `execution location: unknown` rather than guessing.
3. Identify one **editor or notebook environment** you already have access to. If you ran the QAI.00.05 notebook, note its execution location as local, cloud, or unknown; do not assume “browser tab” implies local execution.
4. Locate one **non-sensitive exercise file** you are authorised to use. Record whether it remains on your computer or must be uploaded to a service before a lab works. Do not upload real student, employer, or client records as a setup test.
5. In a service's account/settings screen, distinguish the **signed-in account** from a **credential** and from a non-secret **configuration choice**, such as a model name. Do not create or reveal an actual access key for this exercise.
6. Fill the record below, then compare it with the worked example. For the QAI.00.05 lab, replace any `unknown` relevant to execution or data location before claiming it ran reproducibly.

```text
Machine and OS (general):
Browser:
Editor/notebook:
Where my code executes (local/cloud/unknown):
Where the exercise data lives (local/cloud/unknown):
Is a remote account required? (yes/no/unknown):
One non-secret setting:
One credential type I must protect (type only, not value):
Sensitive data uploaded? (none / describe approved data category only):
Possible cost or usage limit (none/unknown/known limit):
Actual result of one safe check:
Uncertainty to resolve before a larger lab:
```

**Worked reference example:**

```text
Machine and OS (general): Windows laptop
Browser: an installed web browser
Editor/notebook: local Python notebook
Where my code executes: local laptop (confirmed from local notebook runtime)
Where the exercise data lives: local exercise folder containing only fictional course facts
Is a remote account required?: no, for this local exercise
One non-secret setting: exercise data version course_facts_v1
One credential type I must protect: computer login password (value never recorded)
Sensitive data uploaded?: none
Possible cost or usage limit: no paid cloud service used for this exercise
Actual result of one safe check: QAI.00.05 first cell displayed the approved fictional deadline
Uncertainty to resolve before a larger lab: how to install and record Python packages
```

This example describes one possible setup. If the notebook is **hosted**, change `Where my code executes` and perhaps `Where the exercise data lives` to cloud, after checking the provider's actual behavior; keep the browser on the local laptop. Do not copy the reference record if it does not match what you observed.

### 17.2 Solved classification and troubleshooting

| Observation | What it means | First safe action |
|---|---|---|
| Browser page is visible, but a hosted notebook says “runtime disconnected.” | Page is local display; code execution depends on a remote session. | Check service connection/status and save permitted work; avoid assuming code ran. |
| A script says its data file is missing. | Code exists, but data may be in another folder or only on another machine. | Confirm the intended file's location and the notebook's execution location; do not guess a random path. |
| A model service says “not authorised.” | The request lacks permitted access or is using the wrong account/configuration. | Check account and permissions without showing the key value in logs or chat. |
| The lab runs locally but a colleague cannot run it. | Their packages, operating system paths, or files may differ. | Compare recorded environment, data, code, and settings before changing the program. |
| A cloud notebook remains active after class. | Its resources or storage may persist and incur cost under that account. | Review the provider's live resources and usage controls; stop unused compute when appropriate. |

**Case check 1:** A learner opens a cloud notebook in Chrome on a Windows laptop. Where is the browser? Where does Python run? **Solution:** Browser on the local Windows laptop; Python on the cloud notebook's remote runtime. Uploaded data may also be remote. Confirm the service's storage location separately.

**Case check 2:** A screenshot shows `MODEL_PROVIDER_API_KEY=abc123...`. Is the variable *name* secret, or is the *value* the problem? **Solution:** The generic variable name normally is not secret. The value may grant access and must be removed from shared material; if a real key was exposed, rotate/revoke it under the provider's procedure. Do not share the rest of the value when asking for help.

**Case check 3:** The QAI.00.05 lookup lab uses only a local fictional dictionary and a local Python notebook. Is a model-provider API key needed? **Solution:** No; it uses no remote model service. Adding a key would add complexity and exposure without helping the exercise.

### 17.3 Move-ahead condition for this node

You can identify your machine, OS, browser, editor/notebook, code execution location, data location, account, and secret category for one actual setup. You have written an observed result and a remaining uncertainty without exposing secret values. Detailed terminal commands, Python installation, and Git operations belong to QAI.01; this node requires recognition and safe inspection, not memorising commands.

## 18. What to remember

- The working environment is the complete place where code, files, accounts, settings, and services operate.
- Local runs on your computer; cloud runs on provider resources over the internet.
- A notebook is for interactive explanation and experimentation; scripts/packages support repeatable/reusable programs.
- An account identifies access; a credential proves access; a secret must be protected.
- An API key is a secret. Never publish, screenshot, commit, or paste it into shared content.
- Environment variables keep secrets/configuration outside shared code, but access still needs proper security.
- Start small, know where work runs, know what data/cost/access is involved, and record your setup.

## 19. Next connection

The next subsection, `QAI.00.07 — Responsible AI and verification`, establishes the decisions that must surround every AI system: privacy, consent, copyright/licence, fairness, bias, safety, accountability, source checking, test cases, and human review.
