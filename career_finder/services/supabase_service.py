from supabase import create_client, Client
from django.conf import settings
import logging

# Initialize logger and Supabase client
logger = logging.getLogger(__name__)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

def update_supabase_data(career_pages):
    upsert_data = []
    for row in career_pages:
        if isinstance(row, dict):
            mapped_row = {
                'id': row.get('id'),
                'company_type': row.get('company_type'),
                'company_name': row.get('company_name'),
                'url': row.get('url'),
                'careers': row.get('careers'),
                'size': row.get('size'),
                'status': row.get('status'),
                'notes': row.get('notes'),
                'roles': row.get('roles'),
                'user_rank': row.get('user_rank', None) if row.get('user_rank') != '' else None,
                'career_page_url': row.get('career_page_url')
            }
            upsert_data.append(mapped_row)
        else:
            logger.error(f"Row is not a dictionary: {row}")

    supabase.table('companies').upsert(upsert_data).execute()
    return True, None

def fetch_supabase_companies():
    query_result = supabase.table('companies').select('*').execute()
    return query_result.data, None

def add_role_data(company_id, role_title, role_link, salary, score):
    table = "roles"
    data = {
        "company_id": company_id,
        "role_title": role_title,
        "role_link": role_link,
        "salary": salary,
        "score": score
    }
    supabase.table(table).insert([data]).execute()
    return True, None

def fetch_roles_by_company_id(company_id):
    table = "roles"
    roles = supabase.table(table).select("*").eq("company_id", company_id).execute()
    return roles.data, None