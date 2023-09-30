from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadCSVForm
from .services.career_page_finder import find_career_page
from .services.supabase_service import (
    update_supabase_data, 
    fetch_roles_by_company_id, 
    fetch_supabase_companies,
    add_role_data,
    fetch_roles_for_multiple_companies
)
from .services.dives import find_and_add_roles_from_dives
from urllib.parse import urljoin
import csv
import io
import logging
import json

logger = logging.getLogger(__name__)

def fetch_companies_data(request):
    try:
        companies, _ = fetch_supabase_companies()
        companies_data = [{'id': company['id'], 
                           'company_name': company['company_name'], 
                           'url': company['url'], 
                           'careers': company['careers'], 
                           'roles': company['roles']} 
                          for company in companies]
        return JsonResponse({'status': 'success', 'data': companies_data})
    except Exception as e:
        logger.error(f"Exception in fetch_companies_data: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def start_scraping(request):
    if request.method == 'POST':
        selected_rows = json.loads(request.body.decode('utf-8')).get('selectedRows', [])
        for row in selected_rows:
            find_and_add_roles_from_dives(row['id'], row['url'])
        return JsonResponse({'status': 'success'})

def role_call(request):
    try:
        companies, _ = fetch_supabase_companies(limit=20)
        company_ids = [company['id'] for company in companies]
        all_roles, _ = fetch_roles_for_multiple_companies(company_ids)

        return render(request, 'career_finder/role_call.html', {
            'companies': companies,
            'roles': all_roles
        })
    except Exception as e:
        logger.error(f"Exception in role_call: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})

def index(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            csv_data = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(csv_data)
            reader = csv.DictReader(io_string)
            for row in reader:
                if 'url' in row and 'company_name' in row:
                    career_url = find_career_page(base_url=row['url'], row=row)
                    if career_url:
                        complete_career_url = urljoin(row['url'], career_url)
                        row['career_page_url'] = complete_career_url
                        update_supabase_data([row])
            return JsonResponse({'status': 'complete'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form'})
    else:
        return render(request, 'career_finder/index.html', {
            'form': UploadCSVForm()
        })
