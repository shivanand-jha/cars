# Deployment Notes

The app has no external dependencies and can run on any platform that supports a Python web process.

## Local

```bash
python3 app.py
```

Open `http://127.0.0.1:8000`.

## Render / Railway / similar

Use this start command:

```bash
HOST=0.0.0.0 python3 app.py
```

The app reads `PORT` from the environment, so hosted platforms can inject their assigned port automatically.

Recommended settings:

- Runtime: Python 3
- Build command: leave empty
- Start command: `HOST=0.0.0.0 python3 app.py`
- Persistent disk: optional; without it, saved shortlists reset when the service restarts

## Why SQLite is acceptable here

The assignment asks for a working full-stack MVP with non-trivial backend behavior. SQLite gives local persistence with no setup. For a production version, saved shortlists should move to a managed database.
