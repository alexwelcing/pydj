from supabase import create_client, Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

def update_supabase_data(career_pages):
    try:
        upsert_data = []
        for row in career_pages:
            # Make sure row is a dictionary
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

        query_result = supabase.table('companies').upsert(upsert_data).execute()


    except Exception as e:
        logger.error(f"Exception in update_supabase_data: {e}")