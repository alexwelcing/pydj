from functools import lru_cache
import logging
from typing import Iterable, Optional

from django.conf import settings
from supabase import Client, create_client

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_supabase_client() -> Client:
    """Create (and memoize) a Supabase client using Django settings.

    The memoization keeps the expensive HTTP session warm across calls while also
    making it easy to raise a helpful error if environment variables are
    missing.
    """

    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise RuntimeError(
            "Supabase credentials are missing. Set SUPABASE_URL and SUPABASE_ANON_KEY in your environment."
        )

    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)


def update_supabase_data(career_pages: Iterable[dict]):
    try:
        client = _get_supabase_client()
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

        client.table('companies').upsert(upsert_data).execute()
        return True, None
    except Exception as e:
        logger.error(f"Exception in update_supabase_data: {e}")
        return False, str(e)


def fetch_supabase_companies(limit: Optional[int] = None):
    client = _get_supabase_client()
    query = client.table('companies').select('*').order('id', desc=True)
    if limit:
        query = query.limit(limit)
    query_result = query.execute()
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
    _get_supabase_client().table(table).insert([data]).execute()
    return True, None


def fetch_roles_by_company_id(company_id):
    table = "roles"
    roles = _get_supabase_client().table(table).select("*").eq("company_id", company_id).execute()
    return roles.data, None


def fetch_roles_for_multiple_companies(company_ids):
    try:
        if not company_ids:
            return [], None

        roles = _get_supabase_client().table("roles").select("*").in_("company_id", company_ids).execute()
        return roles.data, None
    except Exception as e:
        logger.error(f"Exception in fetch_roles_for_multiple_companies: {e}")
        return [], str(e)


def fetch_supabase_company(company_id: int):
    try:
        result = _get_supabase_client().table('companies').select('*').eq('id', company_id).limit(1).execute()
        if result.data:
            return result.data[0], None
        return None, None
    except Exception as e:
        logger.error(f"Exception in fetch_supabase_company: {e}")
        return None, str(e)
