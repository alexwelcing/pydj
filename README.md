# Career Finder (Django + Supabase)

A refreshed take on the original job-tracking helper. Upload a CSV of target companies, mirror them into Supabase, and trigger lightweight scraping to discover career pages and potential roles. Run the app locally (or in Codespaces) and manage data via a CLI-first workflow.

## Features
- CSV ingestion with immediate Supabase upserts.
- Supabase-backed company list with links to detected career pages and tracked roles.
- Triggerable scraping hook (Google "dives") to discover role titles for selected companies.
- Dedicated Role Call view for a quick scan of all stored opportunities.
- CLI-first controls for ingesting CSVs, triggering scraping, and inspecting roles.

## Getting started locally or in Codespaces
1. Create a `.env` based on `.env.example` with your Supabase URL and anon key.
2. Install dependencies (network-restricted environments like Codespaces may need a pre-baked devcontainer image):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server locally:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
4. Use the CLI to manage data without opening the UI:
   ```bash
   # Ingest a CSV and optionally discover career pages on the fly
   python manage.py career_cli ingest data/companies.csv --detect-career-pages

   # List the latest companies and include any scraped roles
   python manage.py career_cli list --limit 25 --include-roles

   # Trigger Google Dives scraping for specific companies (repeat flag allowed)
   python manage.py career_cli scrape --company-id 1 --company-id 2
   ```
5. Open the app at `http://localhost:8000/` (Codespaces: `https://<workspace>-8000.app.github.dev/`) to use the refreshed uploader and Role Call UI.

## Supabase schema expectations
- `companies` table with columns: `id`, `company_name`, `url`, `career_page_url`, `careers`, `roles`, optional metadata columns like `size`, `status`, `notes`, and `user_rank`.
- `roles` table with `company_id`, `role_title`, `role_link`, `salary`, and `score`.
