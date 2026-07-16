# FinancePro

This repository contains the FinancePro Flet app.

## Local development

1. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the app:
   ```powershell
   python run.py
   ```
4. Open the app in your browser at `http://localhost:10000`.

## Deployment on Render

1. Push this repository to GitHub.
2. Create a new Web Service on Render.
3. Connect it to the GitHub repository and use the `main` branch.
4. Use the default `python` environment.
5. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`
   - Environment Variables: `PORT`, `DATABASE_URL`, `DATABASE_PATH` (optional)

## Database notes

- The app currently uses a local SQLite database under `FinancePro/database/finance.db` by default.
- On Render, the file system is ephemeral, so data will not persist across deploys or instance restarts.
- For production use, migrate the app to a hosted database such as Supabase Postgres.

## Supabase

- Supabase is not automatically connected yet.
- To use Supabase, you will need to update the app to use Postgres-compatible SQL and set `DATABASE_URL` or a hosted database driver.
