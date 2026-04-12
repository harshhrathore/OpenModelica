# OpenModelica Simulation Launcher

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.7-green)
![License](https://img.shields.io/badge/License-MIT-purple)

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Building the OpenModelica Executable](#building-the-openmodelica-executable)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Repository Structure](#repository-structure)
- [Architecture](#architecture)
- [Simulation Flags Reference](#simulation-flags-reference)
- [Code Quality](#code-quality)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

**OpenModelica Simulation Launcher** is a desktop GUI application built with Python and PyQt6 that provides a user-friendly interface for launching and monitoring compiled OpenModelica simulation executables.

The application is specifically designed for the **TwoConnectedTanks** model — a classic fluid-dynamics simulation bundled with OpenModelica that models liquid flow between two interconnected tanks. This launcher eliminates the need for command-line knowledge, making OpenModelica simulations accessible to users of all technical levels.

### What Problem Does This Solve?

OpenModelica compiles models into standalone executables that require command-line parameters. This application:
- Provides a graphical interface to configure and run simulations
- Validates input parameters before execution
- Displays real-time simulation output with color-coded logging
- Allows users to abort long-running simulations
- Makes simulation results easily accessible

## Key Features

- **Intuitive GUI** — Clean, modern interface built with PyQt6
- **File Browser** — Easy selection of compiled simulation executables
- **Parameter Configuration** — Set start and stop times with validation (0 ≤ start < stop < 5)
- **One-Click Execution** — Launch simulations with a single button press
- **Real-Time Monitoring** — Watch stdout/stderr output as it happens
- **Color-Coded Logs** — Distinguish between info, success, and error messages
- **Simulation Control** — Abort running simulations at any time
- **Input Validation** — Automatic validation with clear, actionable error messages
- **Cross-Platform** — Works on Windows and Linux (macOS untested)

## Prerequisites

Before you begin, ensure you have the following installed:

| Requirement  | Version                | Purpose                                    |
| ------------ | ---------------------- | ------------------------------------------ |
| Python       | 3.10+                  | Runtime environment (3.8+ minimum)        |
| PyQt6        | 6.7.x                  | GUI framework (installed via pip)         |
| OpenModelica | 1.21+                  | To compile the TwoConnectedTanks model    |
| OS           | Windows 10/11 or Linux | macOS may work but is untested            |

### Checking Your Python Version

```bash
python --version
# or
python3 --version
```

If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).

---

## Quick Start

For experienced users who want to get started immediately:

```bash
# 1. Clone and navigate to the repository
git clone https://github.com/your-org/TwoConnectedTanks-Simulator.git
cd TwoConnectedTanks-Simulator

# 2. Set up virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run the application
python main.py
```

Then use the GUI to browse for your compiled OpenModelica executable and configure the simulation parameters.

---

## Repository Structure

```
TwoConnectedTanks-Simulator/
├── main.py                  # Application entry point
├── app/
│   ├── __init__.py
│   ├── gui/                 # User interface components
│   │   ├── __init__.py
│   │   ├── main_window.py   # Main application window
│   │   ├── widgets.py       # Reusable UI widgets (LogPanel, PathSelector, etc.)
│   │   └── styles.py        # QSS stylesheet and color constants
│   ├── core/                # Business logic
│   │   ├── __init__.py
│   │   ├── runner.py        # Simulation execution in background thread
│   │   └── validator.py     # Input validation and configuration
│   └── utils/               # Utilities
│       ├── __init__.py
│       └── logger.py        # Application logging
├── requirements.txt         # Python dependencies
├── README.md                # This documentation
└── .gitignore               # Git ignore rules
```

### Module Descriptions

| Module                   | Purpose                                                      |
| ------------------------ | ------------------------------------------------------------ |
| `main.py`                | Application entry point that initializes PyQt6 and launches the main window |
| `app/gui/main_window.py` | Main window layout, UI components, and event handling        |
| `app/gui/widgets.py`     | Reusable widgets: PathSelector, LogPanel, SectionCard, HeaderBanner |
| `app/gui/styles.py`      | QSS stylesheet for consistent theming and color definitions  |
| `app/core/runner.py`     | Background thread that executes simulations and streams output |
| `app/core/validator.py`  | Input validation logic and simulation configuration dataclass |
| `app/utils/logger.py`    | Singleton logger for application-wide logging                |

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/TwoConnectedTanks-Simulator.git
cd TwoConnectedTanks-Simulator
```

### Step 2: Create a Virtual Environment

Using a virtual environment is recommended to avoid dependency conflicts.

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` appear in your terminal prompt, indicating the virtual environment is active.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyQt6 (6.7.1) — GUI framework
- pytest (8.3.2) — Testing framework
- pytest-qt (4.4.0) — PyQt testing utilities
- pycodestyle (2.11.1) — PEP 8 style checker
- pylint (3.3.1) — Code quality analyzer

### Step 4: Verify Installation

```bash
python main.py
```

If the GUI window opens successfully, the installation is complete!

---

## Building the OpenModelica Executable

### Step 1: Install OpenModelica

1. Download OpenModelica from [https://openmodelica.org/download/](https://openmodelica.org/download/)
2. Run the installer for your operating system
3. This will install both the OpenModelica compiler and **OMEdit** (the graphical model editor)

### Step 2: Open OMEdit and Load the Model

**Method A: Using the Libraries Browser (Recommended)**

1. Launch **OMEdit**
2. In the left panel, navigate to **Libraries → Modelica → Fluid → Examples**
3. Look for **TwoConnectedTanks** (you can also use the search bar)
4. Double-click the model to open it

**Method B: Opening the .mo File Directly**

1. In OMEdit, go to **File → Open Model/Library File**
2. Navigate to the OpenModelica library directory:
   - **Windows:** `C:\Program Files\OpenModelica1.21.0\lib\omlibrary\Modelica\Fluid\Examples\`
   - **Linux:** `/usr/lib/omlibrary/Modelica/Fluid/Examples/` or `/opt/openmodelica/lib/omlibrary/Modelica/Fluid/Examples/`
3. Select `TwoConnectedTanks.mo` and click **Open**

> **Can't find the library path?** In OMEdit, go to **Tools → Options → Libraries** to see where OpenModelica installed its standard libraries.

### Step 3: Compile the Model

1. With the TwoConnectedTanks model open, click the **Simulate** button in the toolbar (or right-click the model name → **Simulate**)
2. OMEdit will compile the model and generate several files
3. The compilation output will be saved to a working directory:
   - **Windows:** `%APPDATA%\OMEdit\TwoConnectedTanks\`
   - **Linux:** `~/OMEdit/TwoConnectedTanks/`

### Step 4: Locate the Generated Files

After compilation, you'll find these files in the working directory:

| File                                                            | Purpose                                                 |
| --------------------------------------------------------------- | ------------------------------------------------------- |
| `TwoConnectedTanks.exe` (Windows) / `TwoConnectedTanks` (Linux) | The simulation executable                               |
| `TwoConnectedTanks_init.xml`                                    | Initial values and configuration (required at runtime)  |
| `TwoConnectedTanks_info.json`                                   | Model metadata                                          |
| `*.dll` (Windows) / `*.so` (Linux)                              | Shared libraries (OpenModelica runtime, SUNDIALS, etc.) |

### Step 5: Prepare the Executable

**Important:** Keep all generated files in the same directory. The executable requires the XML and JSON files to be present in its working directory.

**On Linux only:** Make the executable file executable:

```bash
chmod +x TwoConnectedTanks
```

**Verification:** Try running the executable from the command line to ensure it works:

```bash
# Windows
TwoConnectedTanks.exe -override=startTime=0,stopTime=4

# Linux
./TwoConnectedTanks -override=startTime=0,stopTime=4
```

If you see simulation output, the executable is ready to use with the launcher!

---

## Running the Application

### Starting the Launcher

1. Ensure your virtual environment is activated:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/macOS
   source .venv/bin/activate
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. The GUI window will open immediately

### First-Time Setup

When you first launch the application:
1. Click **Browse...** to select your compiled `TwoConnectedTanks` executable
2. The application will remember this path for future sessions
3. Configure your simulation parameters (start and stop times)
4. Click **▶ Run Simulation** to begin

---

## Usage Guide

### Application Interface

The application window consists of several sections:

```
┌─────────────────────────────────────────────────────────────┐
│  🔬 OpenModelica Simulation Launcher                        │
│     Execute compiled TwoConnectedTanks simulations          │
├─────────────────────────────────────────────────────────────┤
│  SIMULATION CONFIGURATION                                   │
│                                                             │
│  Executable Path  [ /path/to/TwoConnectedTanks  ] [Browse] │
│  Start Time (s)   [ − ] [ 0 ] [ + ]                        │
│  Stop Time  (s)   [ − ] [ 4 ] [ + ]                        │
├─────────────────────────────────────────────────────────────┤
│               [ ▶  Run Simulation ]  [ ■ Stop ]            │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (progress bar, visible while running)    │
├─────────────────────────────────────────────────────────────┤
│  Logs                                           [Clear Log] │
│  SIMULATION OUTPUT                                          │
│  [10:42:01] Starting simulation: /path/to/…                │
│  [10:42:01] LOG_SUCCESS: Simulation initialized            │
│  [10:42:02] Simulation finished successfully (exit 0).     │
│  [10:42:02] Output saved to: TwoConnectedTanks_res.mat     │
├─────────────────────────────────────────────────────────────┤
│  Status: Finished (exit 0)                                  │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Instructions

#### 1. Select the Executable

- Click **Browse...** to open a file picker
- Navigate to your compiled `TwoConnectedTanks` executable
- Alternatively, type or paste the full path directly into the text field

#### 2. Configure Simulation Parameters

**Start Time:**
- Use the **−** and **+** buttons to adjust the value
- Or click in the number field and type directly
- Valid range: **0 to 3** (inclusive)
- Default: **0**

**Stop Time:**
- Use the **−** and **+** buttons to adjust the value
- Or click in the number field and type directly
- Valid range: **1 to 4** (inclusive)
- Default: **4**

> **Important Constraint:** Start time must be less than stop time, and both must satisfy: `0 ≤ startTime < stopTime < 5`

#### 3. Run the Simulation

- Click **▶ Run Simulation**
- The application will validate your inputs first
- If validation fails, an error dialog will explain the issue
- If validation succeeds, the simulation starts immediately

#### 4. Monitor Progress

- Watch real-time output in the log panel
- Color-coded messages help distinguish:
  - **Purple** — Informational messages
  - **Green** — Success messages
  - **Red** — Error messages
  - **Gray** — Standard output
- A progress bar appears at the bottom while running
- The status bar shows the current state

#### 5. Stop or Wait for Completion

- To abort a running simulation, click **■ Stop**
- Otherwise, wait for the simulation to complete
- When finished, the status bar shows:
  - `Finished (exit 0)` — Success
  - `Failed (exit N)` — Error (N is the exit code)

#### 6. View Results

- Successful simulations generate a `.mat` file (MATLAB format)
- The log panel shows the output file location
- Example: `TwoConnectedTanks_res.mat`
- This file contains time-series data for all model variables

### Understanding Log Messages

| Message Type | Color  | Example                                      |
| ------------ | ------ | -------------------------------------------- |
| Info         | Purple | `Starting simulation: /path/to/executable`   |
| Success      | Green  | `Simulation finished successfully (exit 0).` |
| Error        | Red    | `Simulation exited with non-zero code: 1.`   |
| Stdout       | Gray   | `LOG_SUCCESS: Simulation initialized`        |
| Stderr       | Red    | `ERROR: Failed to read init file`            |

### Common Validation Errors

| Error Message                                  | Solution                                                |
| ---------------------------------------------- | ------------------------------------------------------- |
| "Executable path is empty"                     | Select an executable using the Browse button            |
| "Executable not found"                         | Verify the file path is correct and the file exists     |
| "The file is not executable" (Linux)           | Run `chmod +x <path>` to grant execute permission       |
| "Start time must be >= 0"                      | Set start time to 0 or higher                           |
| "Stop time must be < 5"                        | Set stop time to 4 or lower                             |
| "Start time must be strictly less than stop time" | Ensure start time is less than stop time             |

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

### Design Overview

The application follows a clean separation of concerns with three main layers:

1. **GUI Layer** (`app/gui/`) — User interface components and styling
2. **Core Layer** (`app/core/`) — Business logic for validation and execution
3. **Utils Layer** (`app/utils/`) — Shared utilities like logging

### Class Diagram

```
main.py
  └─ MainWindow(QMainWindow)
        ├─ PathSelectorWidget(QWidget)   — File path input + browse button
        ├─ QSpinBox × 2                  — Start/stop time inputs
        ├─ LogPanel(QWidget)             — Color-coded output display
        ├─ SimulationRunner(QThread)     — Background subprocess execution
        │     signals: output(str)       — Emits stdout lines
        │              error(str)        — Emits stderr lines
        │              finished(int)     — Emits exit code
        │     uses: SimulationConfig     — Configuration dataclass
        └─ InputValidator                — Static validation methods
              raises: ValidationError    — Custom exception

AppLogger (singleton)                   — Application-wide logging
```

### Component Responsibilities

| Module                   | Class/Component                                                 | Responsibility                                      |
| ------------------------ | --------------------------------------------------------------- | --------------------------------------------------- |
| `main.py`                | `main()`                                                        | Application entry point, PyQt6 initialization       |
| `app/gui/main_window.py` | `MainWindow`                                                    | Main window layout, event handling, state management |
| `app/gui/widgets.py`     | `PathSelectorWidget`                                            | File path input with browse button                  |
|                          | `LogPanel`                                                      | Color-coded log display with timestamps             |
|                          | `SectionCard`                                                   | Styled container for UI sections                    |
|                          | `HeaderBanner`                                                  | Application title and description                   |
| `app/gui/styles.py`      | Constants & QSS                                                 | Color palette and stylesheet definitions            |
| `app/core/runner.py`     | `SimulationRunner`                                              | Execute simulation in background thread             |
| `app/core/validator.py`  | `InputValidator`                                                | Validate user inputs before execution               |
|                          | `SimulationConfig`                                              | Dataclass for simulation configuration              |
|                          | `ValidationError`                                               | Custom exception for validation failures            |
| `app/utils/logger.py`    | `AppLogger`                                                     | Singleton logger for application-wide logging       |

### Key Design Patterns

- **Singleton Pattern** — `AppLogger` ensures a single logging instance
- **Observer Pattern** — PyQt6 signals/slots for event-driven communication
- **Thread Pattern** — `SimulationRunner` runs in a separate thread to prevent UI blocking
- **Dataclass Pattern** — `SimulationConfig` provides immutable configuration
- **Validation Pattern** — `InputValidator` centralizes all validation logic

---

## Code Quality

This project follows professional Python development standards:

### Coding Standards

- **PEP 8 Compliance** — All code formatted to 88-character line length (Black-compatible)
- **Type Hints** — Every function signature includes type annotations (PEP 484)
- **Docstrings** — Google-style docstrings on all classes and public methods
- **Object-Oriented Design** — Clean separation of concerns with single-responsibility classes
- **Explicit Imports** — No wildcard imports; all dependencies are explicit
- **Constants** — Defined in `UPPER_SNAKE_CASE` at module level for clarity

### Running Code Quality Tools

**Check PEP 8 compliance:**
```bash
pycodestyle app/ main.py --max-line-length=88
```

**Run Pylint analysis:**
```bash
pylint app/ main.py
```

**Run tests (if available):**
```bash
pytest tests/ -v
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Executable not found" error

**Cause:** The file path is incorrect or the file doesn't exist.

**Solution:**
- Verify the path is correct
- Ensure you're pointing to the executable file, not the `.mo` source file
- Check that all files from the compilation are in the same directory

#### Issue: "The file is not executable" (Linux only)

**Cause:** The file doesn't have execute permissions.

**Solution:**
```bash
chmod +x /path/to/TwoConnectedTanks
```

#### Issue: Simulation fails immediately with exit code 1

**Cause:** Missing initialization files or incorrect working directory.

**Solution:**
- Ensure `TwoConnectedTanks_init.xml` is in the same directory as the executable
- Verify all `.dll` (Windows) or `.so` (Linux) files are present
- Try running the executable manually from the command line to see detailed error messages

#### Issue: GUI doesn't open or crashes on startup

**Cause:** PyQt6 installation issue or missing dependencies.

**Solution:**
```bash
# Reinstall PyQt6
pip uninstall PyQt6
pip install PyQt6==6.7.1

# Verify installation
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"
```

#### Issue: "Start time must be strictly less than stop time"

**Cause:** Invalid parameter configuration.

**Solution:**
- Ensure start time < stop time
- Both values must satisfy: `0 ≤ startTime < stopTime < 5`
- Example valid configuration: start=0, stop=4

#### Issue: No output appears in the log panel

**Cause:** The simulation may be running but not producing output, or output buffering.

**Solution:**
- Wait a few seconds for output to appear
- Check the status bar for simulation state
- Verify the executable works by running it manually from the command line

### Getting Help

If you encounter issues not covered here:

1. Check the application logs in the terminal where you ran `python main.py`
2. Try running the OpenModelica executable manually to isolate the issue
3. Verify your OpenModelica installation is working correctly
4. Check that all dependencies are installed: `pip list`

---

## Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code:
- Follows PEP 8 style guidelines
- Includes type hints
- Has appropriate docstrings
- Passes all linting checks

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
