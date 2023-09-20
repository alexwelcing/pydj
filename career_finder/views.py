import csv
import io
import json
from urllib.parse import urljoin
from django.shortcuts import render, redirect
from .forms import UploadCSVForm
import requests
from django.http import JsonResponse
from bs4 import BeautifulSoup
import logging
import re
from supabase import create_client, Client
from django.conf import settings

# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

logger = logging.getLogger(__name__)

def update_supabase_data(career_pages):
    for row in career_pages:
        supabase.table('companies').upsert([{
            'company_name': row.get('Company'),
            'url': row.get('URL'),
            'career_page_url': row.get('Career_Page')
        }]).execute()

def deep_crawl(base_url):
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            if any(keyword in a_tag.get_text().lower() for keyword in ['career', 'employment', 'join us', 'work with us', 'job openings']):
                return urljoin(base_url, a_tag['href'])
    except Exception as e:
        return "Deep Crawl Error"

def find_career_page(base_url):
    try:
        response = requests.get(base_url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        career_keywords = ['career', 'careers', 'jobs', 'job', 'vacancies', 'employment', 'work with us', 'join us', 'opportunities', 'hr', 'human resources']
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href'].lower()
            text = a_tag.get_text().lower()
            
            if any(keyword in href or keyword in text for keyword in career_keywords):
                return urljoin(base_url, a_tag['href'])
            
            surrounding_text = a_tag.find_parent().get_text().lower()
            for keyword in career_keywords:
                if re.search(f".{{0,50}}{keyword}.{{0,50}}", surrounding_text):
                    return urljoin(base_url, a_tag['href'])

        return deep_crawl(base_url)
    except Exception as e:
        return "Error"

def index(request):
    processed_count = request.session.get('processed_count', 0)
    career_pages = request.session.get('career_pages', [])
    total_count = len(career_pages)

    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            csv_data = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(csv_data)
            reader = csv.DictReader(io_string)
            total_count = sum(1 for row in reader)
            io_string.seek(0)
            reader = csv.DictReader(io_string)

            for row in reader:
                processed_count += 1
                if 'URL' in row and 'Company' in row:
                    career_url = find_career_page(row['URL'])
                    complete_career_url = urljoin(row['URL'], career_url)
                    row['Career_Page'] = complete_career_url
                    if row not in career_pages:
                        career_pages.append(row)
                    logger.info(f"Success: Found career page for {row['Company']}")
            update_supabase_data(career_pages)
            return JsonResponse({'status': 'complete', 'data': career_pages})
    else:
        form = UploadCSVForm()

    return render(request, 'career_finder/index.html', {'form': form, 'career_pages': career_pages})

def reroll(request, url):
    career_pages = request.session.get('career_pages', [])
    for row in career_pages:
        if row['URL'] == url:
            new_career_url = find_career_page(url)
            row['Career_Page'] = new_career_url
            logger.info(f"Rerolled and found new career URL for {url}")
            break
    update_supabase_data(career_pages)
    return redirect('index')
