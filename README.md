## Endpoints

| Route | Parameters | Returns |
|---|---|---|
| `/health` | none | `{"status": "ok"}` |
| `/` | none | `{"message": "dev-productivity-lab"}` |
| `/version` | none | `{"version": "0.1.0"}` |
| `/add` | `a`, `b` (integers) | `{"result": a + b}` |
| `/multiply` | `a`, `b` (integers) | `{"result": a * b}` |

## Run locally

    pip install -r requirements.txt
    uvicorn app.main:app --reload

## Run the checks

    ruff check . && pytest
