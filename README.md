# OpenModelica Simulation Launcher

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.7-green)
![License](https://img.shields.io/badge/License-MIT-purple)

## Overview

**OpenModelica Simulation Launcher** is a desktop GUI application built with
Python and PyQt6 that provides a user-friendly front-end for launching compiled
OpenModelica simulation executables.

The application is designed around the **TwoConnectedTanks** model — a classic
fluid-dynamics model bundled with OpenModelica that simulates liquid flow
between two tanks connected by a pipe. Compiling this model in OpenModelica
produces a native executable that accepts simulation parameters via command-line
flags. This launcher makes running those simulations accessible without
requiring any command-line knowledge.

### Key capabilities

- Browse for and select the compiled simulation executable
- Configure integer start and stop times (constrained to `0 ≤ start < stop < 5`)
- Launch the simulation with a single click
- Watch real-time stdout/stderr output in a colour-coded log panel
- Abort a running simulation at any time
- Automatic input validation with clear error messages

---

## Repository Structure

```
TwoConnectedTanks-Simulator/
├── main.py                  # Entry point (~8 lines)
├── app/
│   ├── __init__.py
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py   # MainWindow(QMainWindow) — top-level UI
│   │   ├── widgets.py       # Reusable custom widgets
│   │   └── styles.py        # QSS dark theme + colour constants
│   ├── core/
│   │   ├── __init__.py
│   │   ├── runner.py        # SimulationRunner(QThread) — subprocess logic
│   │   └── validator.py     # InputValidator + SimulationConfig dataclass
│   └── utils/
│       ├── __init__.py
│       └── logger.py        # AppLogger singleton (wraps logging)
├── assets/
│   └── icons/               # SVG / PNG icons (optional)
├── tests/
│   ├── test_validator.py    # Validation edge-case tests
│   └── test_runner.py       # Runner signal / subprocess mock tests
├── requirements.txt         # Pinned dependencies
├── README.md                # This file
└── .gitignore
```

---

## Prerequisites

| Requirement  | Version                | Notes                           |
| ------------ | ---------------------- | ------------------------------- |
| Python       | 3.10+                  | 3.8+ minimum; 3.10+ recommended |
| PyQt6        | 6.7.x                  | Installed via pip               |
| OpenModelica | 1.21+                  | Required to compile the model   |
| OS           | Windows 10/11 or Linux | macOS may work but is untested  |

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/TwoConnectedTanks-Simulator.git
cd TwoConnectedTanks-Simulator

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Building the OpenModelica Executable

### Step 1 — Install OpenModelica

Download and install OpenModelica from https://openmodelica.org/download/.
This also installs **OMEdit**, the graphical model editor.

### Step 2 — Load the TwoConnectedTanks model

**Option A — Via OMEdit's built-in Libraries browser (recommended for beginners):**

1. Open **OMEdit**.
2. In the left panel, expand **Libraries → Modelica → Fluid → Examples → DrumBoiler**
   or search directly in the search bar for `TwoConnectedTanks`.
3. Double-click the model to open it.

**Option B — Via File → Open (if you downloaded the `.mo` file separately):**

1. Go to **File → Open Model/Library File**.
2. The `.mo` file is typically found at:
   - **Windows:** `C:\Program Files\OpenModelica1.21.0\lib\omlibrary\`
   - **Linux:** `/usr/lib/omlibrary/` or `/opt/openmodelica/lib/omlibrary/`
3. Navigate to the folder, select the `.mo` file and click **Open**.

> **Tip:** If you cannot find the file, open OMEdit and go to
> **Tools → Options → Libraries** to see the exact path where
> OpenModelica has installed its standard libraries.

### Step 3 — Compile / Build

1. In the model tree, right-click **TwoConnectedTanks** → **Simulate**.
2. Or use the **Build** button in the toolbar.
3. OMEdit will compile the model and produce the following files in a
   working directory (typically `~/OMEdit/TwoConnectedTanks/` on Linux or
   `%APPDATA%\OMEdit\TwoConnectedTanks\` on Windows):

| File                                                            | Purpose                                                 |
| --------------------------------------------------------------- | ------------------------------------------------------- |
| `TwoConnectedTanks` (Linux) / `TwoConnectedTanks.exe` (Windows) | The simulation executable                               |
| `TwoConnectedTanks_init.xml`                                    | Initial values / setup (required at runtime)            |
| `TwoConnectedTanks_info.json`                                   | Model metadata                                          |
| `*.so` / `*.dll`                                                | Shared libraries (OpenModelica runtime, SUNDIALS, etc.) |

### Step 4 — Collect runtime dependencies

Gather the executable **and all files in the same directory** into a single
folder before running the launcher — the executable expects the XML and JSON
files to be in its working directory.

On **Linux**, also ensure the executable is marked executable:

```bash
chmod +x TwoConnectedTanks
```

---

## Running the Application

```bash
python main.py
```

The GUI window will open immediately.

---

## Usage Guide

```
┌─────────────────────────────────────────────────────────────┐
│  OpenModelica Simulation Launcher                           │
│  Execute compiled TwoConnectedTanks simulations …          │
├─────────────────────────────────────────────────────────────┤
│  SIMULATION CONFIGURATION                                   │
│                                                             │
│  Executable Path  [ /path/to/TwoConnectedTanks  ] [Browse] │
│  Start Time (int) [ 0 ▲▼ ]                                 │
│  Stop Time  (int) [ 4 ▲▼ ]                                 │
├─────────────────────────────────────────────────────────────┤
│               [ ▶  Run Simulation ]  [ ■ Stop ]            │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (progress bar, visible while running)    │
├─────────────────────────────────────────────────────────────┤
│  SIMULATION OUTPUT                              [Clear Log] │
│  [10:42:01] Starting simulation: /path/to/…               │
│  [10:42:01] LOG_SUCCESS: …                                 │
│  [10:42:02] Simulation finished successfully (exit 0).     │
├─────────────────────────────────────────────────────────────┤
│  Status bar: Finished (exit 0)                              │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-step

1. **Executable Path** — Click **Browse…** and navigate to the compiled
   `TwoConnectedTanks` executable, or type / paste the path directly.

2. **Start Time** — Use the spin-box arrows or type an integer between
   **0** and **3** (inclusive). Default: `0`.

3. **Stop Time** — Use the spin-box arrows or type an integer between
   **1** and **4** (inclusive). Default: `4`.

   > **Constraint:** `0 ≤ startTime < stopTime < 5`

4. Click **▶ Run Simulation**. The app validates the inputs first:
   - If anything is wrong, a red error dialog explains the issue.
   - If valid, the executable is launched and output streams into the log.

5. While running, the **■ Stop** button is enabled. Click it to abort.

6. When finished, the status bar shows `Finished (exit 0)` (success) or
   `Failed (exit N)` (error).

---

## Simulation Flags Reference

The executable is invoked as:

```
TwoConnectedTanks -override=startTime=X,stopTime=Y
```

The `-override` flag is documented at:
https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/simulationflags.html#simflag-override

It overrides variables defined in the XML setup file at runtime without
recompiling the model. The format is a comma-separated list of `var=value`
pairs:

```
-override=startTime=0,stopTime=4
```

| Variable    | Meaning                   | Allowed range            |
| ----------- | ------------------------- | ------------------------ |
| `startTime` | Simulation start time (s) | 0–3 (must be < stopTime) |
| `stopTime`  | Simulation end time (s)   | 1–4 (must be < 5)        |

---

## Architecture

### Class Diagram

```
main.py
  └─ MainWindow(QMainWindow)
        ├─ PathSelectorWidget(QWidget)   — exe path + browse button
        ├─ QSpinBox × 2                  — startTime, stopTime
        ├─ LogPanel(QWidget)             — coloured output area
        ├─ SimulationRunner(QThread)     — subprocess wrapper
        │     signals: output(str)
        │              error(str)
        │              finished(int)
        │     uses: SimulationConfig (dataclass)
        └─ InputValidator                — static validation methods
              raises: ValidationError

AppLogger (singleton)                   — shared logging.Logger
```

### Module responsibilities

| Module                   | Class                                                           | Responsibility                           |
| ------------------------ | --------------------------------------------------------------- | ---------------------------------------- |
| `app/gui/main_window.py` | `MainWindow`                                                    | Layout, signal wiring, state transitions |
| `app/gui/widgets.py`     | `PathSelectorWidget`, `LogPanel`, `SectionCard`, `HeaderBanner` | Reusable UI components                   |
| `app/gui/styles.py`      | —                                                               | QSS dark theme, colour constants         |
| `app/core/runner.py`     | `SimulationRunner`                                              | Background subprocess, signal emission   |
| `app/core/validator.py`  | `InputValidator`, `SimulationConfig`                            | Pure validation logic + config dataclass |
| `app/utils/logger.py`    | `AppLogger`                                                     | Singleton logger                         |

---

## Code Quality

### Standards applied

- **PEP 8** — all files formatted to 88-character line length (Black-compatible)
- **Type hints** — every function signature annotated (PEP 484)
- **Docstrings** — Google-style docstrings on every class and public method
- **OOP** — four principal classes, each with a single responsibility
- **No wildcard imports** — all imports are explicit
- **Constants** — defined in `UPPER_SNAKE_CASE` at module level

### Running linters

```bash
# PEP 8 style check
pycodestyle app/ main.py --max-line-length=88

# Pylint (target score ≥ 8.5/10)
pylint app/ main.py

# Run tests
pytest tests/ -v
```

---

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
