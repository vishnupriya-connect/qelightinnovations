# QAI.01.01 — Computer and Software Basics

> **Position in the QElight AI path**  
> `QAI.00 Orientation` → **`QAI.01.01 Computer and software basics`** → `QAI.01.02 File-system basics` → terminal, Git, Python, data, AI systems

## 1. Why this comes before Python

Python code, notebooks, models, APIs, and cloud applications all run on computers. Before giving commands or writing code, understand the basic machine picture:

```text
Input + program instructions
          ↓
Computer processes instructions
          ↓
Output, saved files, network requests, or physical action
```

When a program fails, the reason may be in the code, the files, the operating system, the available memory, the network, or permissions. This vocabulary helps locate the problem.

## 2. Computer

- **Computer:** a machine that accepts input, follows instructions, processes information, stores data, and produces output.
- Examples: laptop, desktop, mobile device, remote server, cloud virtual machine.

### Basic input–process–output view

| Part | Example in an AI project |
|---|---|
| input | student question, image, document, code command |
| process | Python program, database query, model inference |
| output | answer, chart, prediction, file, error message |
| storage | notebook, dataset, model file, log, generated image |

## 3. Hardware and software

### Hardware

- **Hardware:** physical parts of a computer that can be touched.
- Examples: keyboard, screen, CPU, GPU, RAM, disk/SSD, network card.

### Software

- **Software:** instructions and data that tell hardware what to do.
- Examples: operating system, browser, Python, code editor, notebook tool, database, AI application.

| Hardware | Software |
|---|---|
| physical machine parts | programs/instructions running on those parts |
| CPU, RAM, disk, GPU | Windows, Python, browser, notebook |
| provides computing capacity | uses that capacity to do work |

**Remember:** software needs hardware to run; hardware needs software/instructions to perform useful work.

## 4. Program

- **Program:** a sequence of instructions written so a computer can perform a task.
- Examples: calculator program, Python script, web application, image-processing tool, AI service.

### Example

```text
Task: calculate total marks

Program instructions:
1. receive marks
2. add marks
3. display total
```

The program may be very small or very large. A GenAI application is also a program/system, even if it calls a model through an API.

## 5. Instruction

- **Instruction:** one specific operation a computer is asked to perform.
- Examples: add two numbers, read a file, show text, call an API, store a result, repeat a step.

### Human language versus computer instruction

| Human request | Computer needs |
|---|---|
| “Prepare student report.” | exact data source, calculation steps, output format, file location, error handling |
| “Find relevant notes.” | query, document source, similarity method, number of results, display rule |

Computers need unambiguous operational instructions. Later, Python gives us a formal way to write them.

## 6. Execution

- **Execution:** the act of a computer running program instructions.
- To **run a program** means to start its execution.

### Example

```text
Python source code exists in a file
        ↓
Python interpreter executes the instructions
        ↓
program produces output, files, errors, or network requests
```

Execution can fail because of incorrect code, missing file, insufficient permission, unavailable package, network error, or lack of memory—not only because the idea was wrong.

## 7. Operating system

- **Operating system (OS):** the main software that manages the computer’s hardware, files, users, permissions, memory, and running programs.
- Examples: Windows, Linux, macOS.

### OS as coordinator

```text
Application / Python program
           ↓
Operating system manages access
           ↓
CPU, memory, storage, network, display
```

The operating system decides how programs access files, memory, and hardware resources. This is why a program may work on one machine and need small setup changes on another.

## 8. Application

- **Application:** software designed for a user task.
- Examples: browser, text editor, spreadsheet, code editor, notebook environment, messaging app, AI chat application.

### Program versus application

| Program | Application |
|---|---|
| any set of executable instructions | user-facing software for a task |
| can be a small internal script | usually provides an interface and workflow |
| e.g., one Python file | e.g., an AI course assistant website |

An application is made from one or more programs, plus interface, data, configuration, and often external services.

## 9. Process

- **Process:** a running instance of a program managed by the operating system.
- A program is the saved instructions; a process is the live running activity.

**Two meanings of “process”:** In QAI.00.01, a task *process* meant the steps from input to output (“read question → find note → answer”). Here, an operating-system *process* means a particular running program using computer resources. One running program may carry out a workflow with many steps. When troubleshooting, ask which meaning is intended.

### Example

```text
Saved file: python.exe / a Python script
Running now: one Python process
```

You can open the same browser multiple times. Each running instance can have one or more processes. Each process uses some memory and CPU time.

### Why it matters later

- a notebook kernel is a running process;
- a web application runs as one or more processes;
- a process can freeze, crash, or consume too much memory;
- stopping/restarting a process can solve certain development problems.

## 10. Memory

- **Memory (RAM):** fast temporary working space used by currently running programs and data.
- Values kept only in a program's RAM are lost when its process ends. RAM itself is reused by other running programs; saving a file explicitly is how the work survives a restart.

### Simple analogy

| Desk while working | Filing cabinet for long-term keeping |
|---|---|
| memory/RAM | storage/disk |
| fast, temporary workspace | slower, persistent place |

### AI example

When you load a large dataset or model, part of it may need to fit in memory. If not enough memory is available, the program may slow down, fail, or need a smaller/batched approach.

## 11. Storage

- **Storage:** persistent place where files and data remain after a program or computer restarts.
- Examples: SSD, hard drive, USB drive, cloud storage.

### AI work stored on disk/cloud

- notebooks and scripts;
- datasets and documents;
- model files/checkpoints;
- generated images/audio/text exports;
- configuration files;
- logs and experiment results.

**Remember:** saving a file writes it to storage. Keeping a value only in a running notebook process keeps that value in memory until the process ends or the value is saved separately. A notebook file may preserve *displayed old output*, but reopening the file does not automatically restore all old live variable values. Restart the notebook runtime and rerun cells in order to check what truly works.

## 12. Processor and CPU

- **Processor:** hardware that performs computations/instructions.
- **CPU (Central Processing Unit):** the general-purpose main processor of a computer.

### CPU is good for

- ordinary program logic;
- file and network work;
- many data-processing tasks;
- development tools, browsers, editors, and small ML workloads.

The CPU does not “understand” the task. It performs operations given by software.

## 13. GPU

- **GPU (Graphics Processing Unit):** processor designed to perform many similar calculations in parallel.
- Originally designed for graphics; now widely used for deep learning and image/video workloads.

### Why GPUs matter for AI

Deep-learning models often perform large matrix/tensor calculations. A suitable GPU can perform many of these operations faster than a general CPU.

| CPU | GPU |
|---|---|
| general-purpose processing | many parallel calculations |
| useful for most programming/startup work | useful for many deep-learning/image workloads |
| usually available in every computer | may be absent, limited, or remote/cloud-based |

### Important practical point

- An API-based GenAI application often does not need your own powerful GPU because the provider runs the large model remotely.
- Training/fine-tuning/running large local models or image-generation workloads may need a suitable GPU and enough memory.
- More GPU is not automatically better; consider task, cost, availability, and data/privacy requirements.

## 14. Local machine

- **Local machine:** the computer directly used by you, such as your laptop or desktop.
- Code/files run or are stored on your own machine.

### Example

```text
You run a Python notebook on your laptop.
The notebook process uses your laptop CPU/RAM.
The file is saved on your laptop storage.
```

## 15. Remote machine

- **Remote machine:** another computer accessed through a network.
- It may be owned by an organisation, a hosting provider, a lab, or a cloud service.

### Example

```text
Your browser/editor on laptop
           ↓ network
Remote server runs the application/model/database
```

Your local machine controls or accesses the remote machine, but the actual computation/storage may happen elsewhere.

## 16. Cloud machine

- **Cloud machine:** a remote computing resource provided on demand through a cloud service.
- A cloud machine is a type of remote machine.

**Remote versus cloud:** any computer accessed over a network is remote relative to you. A rented cloud virtual machine is both remote and cloud-provided. A provider may also offer a managed *service* (such as an online model API) without giving you a machine you can log into and administer. Do not call every remote website “your cloud machine.”

### Common uses in AI work

- hosted notebook with GPU;
- deploy a web/API application;
- store documents/data;
- run scheduled data/model jobs;
- use managed databases, vector search, monitoring, and model services.

### Local, remote, and cloud comparison

| Question | Local machine | Remote machine | Cloud machine |
|---|---|---|---|
| where is it? | with/near you | elsewhere on a network | provider-managed remote infrastructure |
| who manages it? | mainly you | organisation/provider | cloud provider plus you/configuration |
| typical use | learning and small development | organisational server | scalable resources, deployment, GPU/services |
| key concern | local setup/capacity | access/network/permissions | cost, access, configuration, data handling |

## 17. One complete picture: running a GenAI application

```text
Learner uses browser on local laptop
         ↓
Browser sends question to application
         ↓
Application process runs on local or cloud machine
         ↓
Application reads approved documents from storage/database
         ↓
Application calls remote model API or local model
         ↓
Output returns through application to learner browser
```

This picture shows why AI applications need more than a model: machines, software, processes, storage, network, permissions, and controls all participate.

## 18. Practical observation on your own computer

Without changing anything, identify:

- your operating system name;
- one application currently open;
- one file saved in storage;
- one process using memory/CPU;
- whether you are using local software, a remote website, or a cloud notebook;
- one task for which your local machine is enough and one task likely to need cloud/GPU later.

Example:

```text
Local task: write and run a basic Python script.
Cloud/GPU task later: fine-tune or run a large image-generation model.
```

## 19. Hands-on machine-readiness record

Before an AI lab, inspect your machine and record only information relevant to the work.

```text
Operating system and version:
Available storage in intended project drive:
Memory/RAM available while ordinary apps are open:
CPU name:
GPU name, if any:
Network condition for cloud/API work:
Project location to use:
One browser and one editor/notebook environment available:
```

### Diagnose before changing anything

| Symptom | Likely meaning | First safe check | Do not assume |
|---|---|---|---|
| computer becomes slow | too many processes or insufficient memory | inspect running apps and memory use | that a GPU is required |
| drive is full | insufficient storage for data/environments | inspect large authorised files and project location | that deleting random system files is safe |
| notebook/browser closes | memory/resource pressure or application error | note exact action and error; retry with smaller input | that the model itself is broken |
| GPU task does not run | no compatible GPU, driver/runtime issue, or cloud setting | confirm whether the task actually needs a GPU | that every AI task uses GPU |
| remote service fails | network, account, permission, quota, or service issue | read exact error and verify account/network | that rerunning repeatedly will fix it |

### Completion condition

You can explain where your work will run, where files will be stored, what resource is limiting, and what evidence you would collect before seeking help.

### Guided observation on your own machine

Use the computer's built-in system information and running-applications view. Observe; do not change, delete, install, or reveal private information for this exercise.

1. Write the operating system name and whether the exercise computer is your own **local** machine or a **remote** one.
2. Open a browser or notebook and identify its running application/process in the machine's running-applications view. Observe whether its memory use changes while the application opens and closes; exact numbers are not required.
3. Find one fictional or non-sensitive practice file. Confirm that it remains on **storage** after closing the app that viewed it. This observation distinguishes saved data from a live process.
4. If you used the QAI.00.05 Python example, say whether the code ran on your local machine or in a remote notebook. Identify which machine supplied the CPU/RAM for that run. Do not guess from where the browser window appears.
5. Complete the readiness record in §19 using only general non-sensitive facts and one observed result. The learner's actual observation is evidence; the sample below is a *worked example*, not a description of your computer.

**Worked example — fictional learner:**

```text
Operating system: Windows on a local laptop
Application and process observed: web browser open, using memory while running
Processor: CPU available for a small notebook; exact model recorded from system information if needed
Memory: enough for the small fictional QAI.00.05 lookup lab; not tested for a large local model
Storage: practice notebook saved in a known learner folder and still present after closing browser
GPU: not established; not required for the small lookup exercise
Network: not needed for local lookup; needed to contact a remote model provider
Code execution location: local Python notebook for this example
Expected observation: browser uses RAM while open; saved practice file remains after it closes
Actual observation: browser closed; practice file still visible on storage
Unresolved question: actual memory and GPU capacity for future large-model work
```

**Do not generalise from this sample:** A different learner may see a browser on their laptop and a cloud notebook runtime elsewhere. In that case the browser uses local resources while notebook code uses remote CPU/RAM; files may be remote unless separately saved locally.

### Solved diagnosis practice

| Symptom | Identify the likely category | First evidence to collect | Explanation |
|---|---|---|---|
| A notebook reopens and shows yesterday's answer, but the first newly run cell says a variable is unknown. | Saved notebook output versus live process memory | Restart runtime, rerun cells from the beginning, and record the first failing cell | Old displayed output persisted in the file; the old live variable did not. |
| The browser displays a hosted notebook, but code stops when internet access is lost. | Local display, remote execution/network | Check whether its runtime is remote and whether the service reports disconnected | The local browser can remain open while the remote execution connection fails. |
| A script cannot save a generated image even though memory is available. | Storage/permission or path, not necessarily RAM | Inspect intended save location, free disk space, and permission/error text | Saving writes to storage; available RAM alone cannot guarantee a file can be saved. |
| A two-line calculator runs without a GPU. | CPU versus GPU | Record what task ran and its actual result | A GPU is not a prerequisite for ordinary calculations or beginner Python work. |

### Quick check, with answers

1. **Question:** Are a saved `.py` file and a running Python process the same thing? **Answer:** No. The file stores program instructions; the process is one live execution of them.
2. **Question:** Is every remote website a cloud machine that the learner controls? **Answer:** No. A remote site can be an application or managed service. A cloud virtual machine is one kind of provider-supplied remote resource.
3. **Question:** An AI app calls a remote model service. Does the learner's laptop need a GPU to run the large remote model? **Answer:** Usually no; the provider runs that model on its own compute. The learner's machine still needs suitable local resources and a network connection for the app.
4. **Question:** A learner saves a notebook, restarts its runtime, and sees old output. Are all old program variables restored? **Answer:** Not necessarily. Run the cells in order or load deliberately saved data to reconstruct live state.

## 20. What to remember

- Hardware is physical; software is instructions/programs that use hardware.
- A program contains instructions; execution means running them.
- An operating system manages hardware, files, processes, memory, and permissions.
- A process is a program currently running.
- Memory/RAM is temporary workspace; storage keeps files after restart.
- CPU is general-purpose processor; GPU is useful for many parallel AI calculations.
- Local machine is yours; remote machine is elsewhere; cloud machine is provider-managed remote computing.
- AI applications are systems: browser, program/process, storage/data, model/service, network, and user all work together.

## 21. Next connection

Next: `QAI.01.02 — File-system basics`. You will learn how computers organise the files and folders that hold code, notebooks, datasets, configuration, models, and project evidence.
