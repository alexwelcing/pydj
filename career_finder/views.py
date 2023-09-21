from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .forms import UploadCSVForm
from .services.career_page_finder import find_career_page
from .services.supabase_service import update_supabase_data
import csv
import io
import logging
from urllib.parse import urljoin
from .services.dives import google_search_and_scrape
from django.views.decorators.csrf import csrf_exempt
from .services.supabase_service import fetch_supabase_companies
from supabase import create_client, Client
import json


# Initialize logging
logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

def fetch_companies(request):
    try:
        logger.info("About to fetch companies from Supabase.")
        companies, error = fetch_supabase_companies()
        
        if error is None:
            return JsonResponse({'status': 'success', 'data': companies})
        else:
            logger.error(f"Error fetching companies: {error}")
            return JsonResponse({'status': 'error', 'message': error})
    except Exception as e:
        logger.error(f"Exception in fetch_companies: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def start_scraping(request):
    try:
        if request.method == 'POST':
            selected_rows = json.loads(request.body.decode('utf-8')).get('selectedRows', [])
            for row in selected_rows:
                google_search_and_scrape(row['base_url'], row)
            return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def role_call(request):
    return render(request, 'career_finder/role_call.html')

def index(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            csv_data = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(csv_data)
            reader = csv.DictReader(io_string)
            
            # Process each row and update the database immediately
            for row in reader:  # Now, 'row' should be a dictionary
                if 'url' in row and 'company_name' in row:
                    career_url = find_career_page(base_url=row['url'], row=row)
                    complete_career_url = urljoin(row['url'], career_url)
                    row['career_page_url'] = complete_career_url  # Updating the 'career_page_url' column

                    # Update the Supabase database right away
                    update_supabase_data([row])  # Sending a list containing the single row
                    
                    logger.info(f"Success: Found career page for {row['company_name']} and updated the database.")
            
            return JsonResponse({'status': 'complete'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form'})
    else:
        form = UploadCSVForm()

    return render(request, 'career_finder/index.html', {'form': form, 'role_call_link': '/role_call'})
