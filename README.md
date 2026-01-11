# verity-quick-demo
[![Python application](https://github.com/Verity-Foundation/verity-quick-demo/actions/workflows/python-app.yml/badge.svg)](https://github.com/Verity-Foundation/verity-quick-demo/actions/workflows/python-app.yml)[![Pylint](https://github.com/Verity-Foundation/verity-quick-demo/actions/workflows/pylint.yml/badge.svg)](https://github.com/Verity-Foundation/verity-quick-demo/actions/workflows/pylint.yml)

This repository contains a small demo of Verity protocol components: a CLI for creating DID documents and verifiable claims, signing them, and storing claims using a mock IPFS/registry middleware. The code is intentionally small and focused on demonstrating the core flows: claim generation, signing, and storing.

## Goals

- Demonstrate claim creation from a short message or a file (without embedding large files in the claim)
- Sign claims with a local private key (demo only)
- Store the signed claim via a mock IPFS gateway
- Keep the code simple, readable and maintainable

## Prerequisites

- Python 3.11+ (tests used with 3.13 in CI)
- Install dependencies:
  - pydantic
  - requests
  - eth-account
  - fastapi
  - uvicorn
  - pytest (for running tests)

## Quick start — Interactive CLI

### 1.Open a Python virtual environment and install deps (example)

```bash
python -m venv .venv
source .venv/Scripts/activate  # on Windows use: .venv\\Scripts\\activate
pip install -r requirements
```

### 2.Run Servers(In another terminal)

```bash
./demo.sh 
```

### 3.Run UI

```bash
python ui_main.py 
```

### 4.Run CLI

```bash
python cli_main.py 
```

Follow prompts to create an account, create DID documents, sign messages, and store documents.

## Testing

### Run the unit tests

```bash
pytest -q src/
```

### Project structure (relevant files)

- `src/cli/` — interactive CLI and headless entrypoint
- `src/middleware/` — simple client for registry/IPFS mocks (with timeouts, retries and pydantic returns)
- `src/core/` — contains all core requirements (models, exceptions, io, crypto...)
- `src/backend/` — Interact with all Services and client
- `src/*_test.py` — unit tests for the components
- `src/services/` — Contains all additionnal services
