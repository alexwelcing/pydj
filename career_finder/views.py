from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UploadCSVForm
from .services.career_page_finder import find_career_page
from .services.supabase_service import update_supabase_data
import csv
import io
import logging
from urllib.parse import urljoin

# Initialize logging
logger = logging.getLogger(__name__)

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

    return render(request, 'career_finder/index.html', {'form': form})
