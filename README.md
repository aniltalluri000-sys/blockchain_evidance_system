# Blockchain Evidence System

A Flask application for recording digital evidence, generating SHA-256 file hashes, and storing evidence metadata in a simple hash-linked blockchain.

## Features

- Upload evidence with a case ID, investigator, and description
- Generate a SHA-256 hash for each uploaded file
- Append evidence hashes to `blockchain.json`
- Store searchable evidence metadata in a local SQLite database
- Verify whether a file matches its stored hash
- View the blockchain and download its JSON representation

## Requirements

- Python 3.10 or newer
- Flask

## Setup

Create and activate a virtual environment, then install Flask:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

```bash
pip install Flask
```

## Run

```bash
python app.py
```

Open <http://127.0.0.1:5000> in a browser.

## Routes

| Route | Purpose |
| --- | --- |
| `/` | Upload evidence and view totals |
| `/evidence` | View stored evidence records |
| `/verify` | Verify an evidence file against its stored hash |
| `/search` | Search records by case ID |
| `/blockchain` | View the hash-linked blockchain |
| `/download` | Download `blockchain.json` |

## Data files

- `blockchain.json` stores the hash-linked chain.
- `evidence.db` is created locally by SQLite when the app starts.
- Uploaded files are stored in `evidence/`.

The repository excludes the local database, uploaded evidence, and Python cache files through `.gitignore`. Do not commit confidential evidence or production data.

## Note

This is an educational project. Before using it for real investigations, add authentication, authorization, secure file handling, input validation, audit logging, encrypted storage, and a production database.