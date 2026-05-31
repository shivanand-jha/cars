# CarDekho Shortlist Coach

A full-stack take-home assignment MVP for helping a confused car buyer move from "I don't know what to buy" to a confidence-ranked shortlist.

## Run locally

```bash
cd /Users/shivanand/react/cardekho
python3 app.py
```

Open `http://127.0.0.1:8000`.

No npm, pip, Docker, or external services are required. The app uses only Python stdlib, browser HTML/CSS/JS, and SQLite.

For deployment notes, see `DEPLOYMENT.md`.

## Deliverable links

- GitHub repo: TODO

## What I built and why

I built a Shortlist Coach: a guided web app that asks for buyer priorities, ranks cars with visible reasoning, lets the buyer compare up to three cars, and saves shortlist sessions with notes.

This directly targets the assignment brief. The buyer does not need another filter table; they need help turning fuzzy priorities like budget, safety, family size, mileage, and city/highway usage into a clear shortlist.

## What I deliberately cut

- Real vehicle inventory ingestion.
- Login/accounts.
- LLM-generated natural language answers.
- Dealer lead capture.
- Full deployment automation.
- Exhaustive tests and production-grade design system.

The goal was a tight 2-3 hour MVP that works end-to-end and shows product judgment.

## Tech stack and why

- Python `http.server`: enough to serve frontend and APIs without dependency setup.
- SQLite: simple persistence for saved shortlist sessions.
- Vanilla HTML/CSS/JS: fast to ship, easy to review, and no build step.
- Embedded seed dataset: keeps the assignment runnable offline and under two minutes.

I picked this stack because the local environment did not have Node/npm or web frameworks available, and the assignment values shipping speed and runnability.

## What AI handled vs. what I handled manually

Delegated to AI:

- Turning the vague brief into a scoped product concept.
- Drafting the scoring model and realistic seed data.
- Generating the backend, frontend, and README structure.
- Creating smoke-test commands and checking obvious failure points.

Handled manually / reviewed:

- Product scope: recommendation and comparison instead of a broad marketplace clone.
- Scoring tradeoffs and whether the explanations help a buyer.
- Keeping the stack dependency-free.
- Reviewing that the backend does non-trivial computation and persistence.

## Where AI helped most

AI helped most with speed: converting the assignment into an implementation plan, creating boilerplate across backend/frontend/README, and keeping the product centered on buyer confidence instead of visual polish.

## Where AI got in the way

AI can overbuild if not constrained. The useful move was cutting features early: no auth, no external APIs, no fancy LLM layer, no heavy framework. The MVP became stronger once the scope was kept small.

## If I had another 4 hours

- Add a richer dataset import path from CSV.
- Add explicit ownership-cost estimates.
- Add a "why not this car" view for rejected options.
- Add shareable shortlist links.
- Deploy to a public URL.
- Add focused backend unit tests around scoring.

## API surface

- `GET /` serves the app.
- `GET /api/cars` returns the seeded dataset.
- `POST /api/recommend` ranks cars from buyer preferences.
- `POST /api/shortlist` saves selected car IDs, preferences, and notes.
- `GET /api/shortlists` returns recent saved sessions.

## Smoke test

Backend logic and persistence can be checked without starting the server:

```bash
python3 smoke_test.py
```

With the server running, the API can also be checked directly:

```bash
curl http://127.0.0.1:8000/api/cars
curl -X POST http://127.0.0.1:8000/api/recommend \
  -H 'Content-Type: application/json' \
  -d '{"budget_lakh":12,"family_size":4,"usage":"mixed","safety_priority":5,"mileage_priority":3,"feature_priority":3,"body_preference":"any"}'
```
