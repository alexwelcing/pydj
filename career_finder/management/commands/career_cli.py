import csv
from pathlib import Path
from urllib.parse import urljoin

from django.core.management.base import BaseCommand, CommandError

from career_finder.services.career_page_finder import find_career_page
from career_finder.services.dives import find_and_add_roles_from_dives
from career_finder.services.supabase_service import (
    fetch_roles_for_multiple_companies,
    fetch_supabase_companies,
    fetch_supabase_company,
    update_supabase_data,
)


class Command(BaseCommand):
    help = "Manage company and role data directly from the CLI (ideal for Codespaces)."

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand", required=True)

        ingest = subparsers.add_parser("ingest", help="Import companies from a CSV into Supabase")
        ingest.add_argument("csv_path", help="Path to the CSV file with company_name and url columns")
        ingest.add_argument(
            "--detect-career-pages",
            action="store_true",
            help="Attempt to find and store the career page for each company while ingesting",
        )

        list_cmd = subparsers.add_parser("list", help="List companies currently in Supabase")
        list_cmd.add_argument("--limit", type=int, default=20, help="Limit the number of rows returned (default: 20)")
        list_cmd.add_argument(
            "--include-roles",
            action="store_true",
            help="Also show role titles grouped by company",
        )

        scrape = subparsers.add_parser("scrape", help="Trigger Google Dives scraping for companies")
        scrape.add_argument(
            "--company-id",
            action="append",
            type=int,
            dest="company_ids",
            help="Specific company IDs to scrape (can be provided multiple times)",
        )
        scrape.add_argument(
            "--limit",
            type=int,
            default=10,
            help="If no company IDs are provided, scrape the latest N companies (default: 10)",
        )

    def handle(self, *args, **options):
        subcommand = options.get("subcommand")
        if subcommand == "ingest":
            self._ingest(options)
        elif subcommand == "list":
            self._list(options)
        elif subcommand == "scrape":
            self._scrape(options)
        else:
            raise CommandError("Unknown subcommand")

    def _ingest(self, options):
        csv_path = Path(options["csv_path"])
        detect_career_pages = options["detect_career_pages"]

        if not csv_path.exists():
            raise CommandError(f"CSV file not found: {csv_path}")

        with csv_path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            missing_columns = {col for col in ["company_name", "url"] if col not in reader.fieldnames}
            if missing_columns:
                raise CommandError(f"CSV missing required columns: {', '.join(sorted(missing_columns))}")

            rows = list(reader)

        if detect_career_pages:
            for row in rows:
                career_url = find_career_page(base_url=row["url"], row=row)
                if career_url and not row.get("career_page_url"):
                    row["career_page_url"] = urljoin(row["url"], career_url)

        success, error = update_supabase_data(rows)
        if not success or error:
            raise CommandError(error or "Failed to upsert company data to Supabase")

        self.stdout.write(self.style.SUCCESS(f"Ingested {len(rows)} companies into Supabase"))

    def _list(self, options):
        limit = options["limit"]
        include_roles = options["include_roles"]

        companies, error = fetch_supabase_companies(limit=limit)
        if error:
            raise CommandError(error)

        if not companies:
            self.stdout.write("No companies found in Supabase")
            return

        company_ids = [company["id"] for company in companies]
        roles_by_company = {}
        if include_roles:
            roles, _ = fetch_roles_for_multiple_companies(company_ids)
            for role in roles:
                roles_by_company.setdefault(role.get("company_id"), []).append(role)

        for company in companies:
            self.stdout.write(
                f"[{company['id']}] {company['company_name']} — {company.get('career_page_url') or company.get('url')}"
            )
            if include_roles:
                for role in roles_by_company.get(company["id"], []):
                    self.stdout.write(f"    • {role.get('role_title')} (score: {role.get('score')})")

    def _scrape(self, options):
        company_ids = options.get("company_ids")
        limit = options["limit"]

        if company_ids:
            companies = []
            for company_id in company_ids:
                company, error = fetch_supabase_company(company_id)
                if error:
                    raise CommandError(error)
                if not company:
                    self.stderr.write(self.style.WARNING(f"Company ID {company_id} not found; skipping"))
                    continue
                companies.append(company)
        else:
            companies, error = fetch_supabase_companies(limit=limit)
            if error:
                raise CommandError(error)

        if not companies:
            self.stdout.write("No companies available to scrape")
            return

        for company in companies:
            target_url = company.get("career_page_url") or company.get("url")
            if not target_url:
                self.stderr.write(self.style.WARNING(f"Company {company['id']} missing URL; skipping"))
                continue

            find_and_add_roles_from_dives(company["id"], target_url)
            self.stdout.write(self.style.SUCCESS(f"Scraped roles for {company['company_name']} ({target_url})"))
