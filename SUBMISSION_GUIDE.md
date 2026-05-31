# Submission Guide

Use this as the final handoff checklist for the CarDekho Group assignment.

## 1. Run the app locally

```bash
cd /Users/shivanand/react/cardekho
python3 app.py
```

Open `http://127.0.0.1:8000`.

## 2. Run the smoke test

In another terminal:

```bash
cd /Users/shivanand/react/cardekho
python3 -B smoke_test.py
```

Expected output:

```text
smoke tests passed
```

## 3. Record the submission walkthrough

The assignment asks for the build process. If a full build recording was not captured, record a transparent walkthrough instead and explain that the build was AI-assisted.

Suggested 6-8 minute structure:

1. Show the PDF assignment and briefly restate the brief.
2. Show `README.md` and the product decision: Shortlist Coach over a marketplace clone.
3. Start the app with `python3 app.py`.
4. Use three buyer profiles:
   - Safety-first family: budget 12L, mixed use, safety 5.
   - Budget commuter: budget 9L, city use, mileage 5, hatchback.
   - Large family: budget 15L, highway use, family size 6+, MPV.
5. Select two or three cars, compare them, add notes, and save the shortlist.
6. Refresh the page and show the saved shortlist remains.
7. Run `python3 -B smoke_test.py`.
8. Show `git log --oneline -3` and explain the remaining README placeholders.

## 4. Push to GitHub

Create an empty GitHub repo, then run:

```bash
cd /Users/shivanand/react/cardekho
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

If GitHub asks for authentication, use your normal browser or token flow.

## 5. Fill README links

Replace the TODO values in `README.md`:

- Screen recording
- GitHub repo
- Live URL, if deployed

If not deploying, leave the local run instructions as the runnable path.

Optional deployment notes are in `DEPLOYMENT.md`.

## 6. Final submission contents

Send:

- Screen recording link
- GitHub repository link
- Live URL or local run instructions
- README included in the repo
