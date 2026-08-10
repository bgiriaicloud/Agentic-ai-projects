# GitHub Actions CI/CD Reference Notes

This document covers GitHub Actions workflow configurations, triggers, runner properties, matrix variables, environment secrets, and artifact caching.

---

## 📋 Table of Contents
*   [Core Concepts & Execution Model](#core-concepts--execution-model)
*   [Workflow File Structure & Syntax](#workflow-file-structure--syntax)
*   [Triggers & Events](#triggers--events)
*   [Environments, Secrets & Variables Context](#environments-secrets--variables-context)
*   [Caching & Build Artifacts](#caching--build-artifacts)
*   [Advanced Strategies (Matrix & Concurrency)](#advanced-strategies-matrix--concurrency)

---

## Core Concepts & Execution Model

GitHub Actions is an API-driven CI/CD orchestration engine. It automates build, test, and deployment pipelines.

```
[ Workflow ] -> contains 1 or more -> [ Jobs ] (run in parallel by default on separate Runners)
                                         |
                                     contains -> [ Steps ] (run sequentially on the same Runner)
                                                    |
                                                runs -> [ Shell Commands / Actions ]
```

*   **Workflow**: A configurable automated process defined in a `.github/workflows/*.yaml` file.
*   **Job**: A set of steps executed on the same runner instance. Jobs run in parallel by default, but you can configure dependencies between them.
*   **Step**: An individual task that runs commands or actions. Steps in a job run sequentially on the same runner, allowing them to share data.
*   **Action**: A reusable application extension that simplifies complex steps (e.g., setting up a Python environment or authenticating with GCP).
*   **Runner**: A virtual machine or container running the GitHub Actions runner agent to execute jobs.
    *   *GitHub-hosted*: Hosted by GitHub (Linux, macOS, Windows) with pre-installed tools.
    *   *Self-hosted*: Hosted on your own infrastructure, useful for accessing private networks.

---

## Workflow File Structure & Syntax

A complete workflow YAML manifest:

```yaml
# .github/workflows/ci.yaml
name: Continuous Integration

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
      # 1. Check out repository code
      - name: Checkout Code
        uses: actions/checkout@v4

      # 2. Set up Python runtime
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      # 3. Install dependencies
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # 4. Run test cases
      - name: Run Test Suite
        run: pytest
```

---

## Triggers & Events

Workflows can be triggered by multiple GitHub events:

### Event Triggers
*   `push`: Runs when commits are pushed to specified branches or tags.
*   `pull_request`: Runs when pull requests are opened, updated, or synchronized.
*   `workflow_dispatch`: Adds a manual "Run workflow" button in the GitHub UI, allowing you to pass custom inputs.
*   `schedule`: Runs on a cron schedule in the background.

```yaml
on:
  # Trigger manually with optional input variables
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target deployment environment'
        required: true
        default: 'staging'
  
  # Trigger on cron schedule (every Sunday at midnight)
  schedule:
    - cron: '0 0 * * 0'
```

---

## Environments, Secrets & Variables Context

GitHub Actions provides several contexts to access variables, secrets, and environment details:

*   **GitHub Token (`${{ secrets.GITHUB_TOKEN }}`)**: An automatic token generated for each workflow run to authenticate API calls without manual configuration.
*   **Secrets (`${{ secrets.SECRET_NAME }}`)**: Encrypted variables that are masked in log outputs.
*   **Vars (`${{ vars.CONFIG_VAR }}`)**: Plaintext configuration variables.
*   **Steps Outputs**: Pass values between steps in a job.

```yaml
steps:
  - name: Generate Output
    id: generator
    run: echo "token=abc123xyz" >> "$GITHUB_OUTPUT"

  - name: Use Output
    run: echo "The token value is ${{ steps.generator.outputs.token }}"
```

---

## Caching & Build Artifacts

### Caching Dependencies
Speed up workflows by reusing downloaded packages (like pip dependencies or node modules) across runs.
```yaml
- name: Cache Pip Packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Uploading & Downloading Artifacts
Pass files (like compiled binaries or build reports) between jobs or download them from the run page.
```yaml
# Job 1: Build and save artifact
- name: Upload Binary
  uses: actions/upload-artifact@v4
  with:
    name: build-artifact
    path: dist/app.bin

# Job 2: Download and use artifact
- name: Download Binary
  uses: actions/download-artifact@v4
  with:
    name: build-artifact
    path: bin/
```

---

## Advanced Strategies (Matrix & Concurrency)

### Matrix Builds
Run a job across multiple configurations (different OS or runtime versions) simultaneously.
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.9', '3.11']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

### Concurrency Limits
Cancel in-progress runs of the same workflow (e.g., when pushing multiple commits in a row) to save action minutes.
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```
