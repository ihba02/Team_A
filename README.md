# Metadata Management API

This small Flask API exposes metadata about data files placed in `src/` (table schemas, load status, and last-updated timestamps).

Files supported: JSON, CSV, XML (detects `*.json`, `*.csv`, `*.xml` in `src/`).

Endpoints:

- `GET /tables` — list available tables (name, file, extension)
- `GET /tables/<table>/schema` — schema (fields and simple inferred types)
- `GET /tables/<table>/status` — presence, row count, and size in bytes
- `GET /tables/<table>/last_updated` — ISO timestamp of last modification
- `GET /metadata/schemas` — schemas for all tables
- `GET /metadata/status` — status for all tables
- `GET /metadata/last_updated` — last-updated timestamps for all tables

How to run locally:

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
```

2. Run the API:

```powershell
python src\app.py
```

3. Open http://127.0.0.1:5000/tables

Notes:

- The app infers simple types (int/float/str) for CSV and JSON fields by sampling values.
- XML schema inference picks child tags of the first record element.
# Team_A
