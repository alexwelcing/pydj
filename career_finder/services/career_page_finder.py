import requests
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import logging
from .supabase_service import update_supabase_data

logger = logging.getLogger(__name__)

def deep_crawl(base_url):
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for a_tag in soup.find_all('a', href=True):
            if any(keyword in a_tag.get_text().lower() for keyword in ['career', 'employment', 'join us', 'work with us', 'job openings']):
                return urljoin(base_url, a_tag['href'])
    except Exception as e:
        logger.error(f"Deep crawl error: {e}")
        return "Deep Crawl Error"

def find_career_page(base_url, row):
    try:
        time.sleep(3)  # rate limiting
        response = requests.get(base_url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href'].lower()
            text = a_tag.get_text().lower()
            
            if any(keyword in href or keyword in text for keyword in ['career', 'careers', 'jobs', 'job', 'vacancies', 'employment', 'work with us', 'join us', 'opportunities', 'hr', 'human resources']):
                career_url = urljoin(base_url, a_tag['href'])
                row['career_page_url'] = career_url  # Now aligned with the Supabase column
                update_supabase_data([row])  # Passing a list containing the single dictionary
                return career_url
                
        deep_url = deep_crawl(base_url)
        row['career_page_url'] = deep_url  # Now aligned with the Supabase column
        update_supabase_data([row])  # Passing a list containing the single dictionary
        return deep_url
    except Exception as e:
        logger.error(f"Error finding career page: {e}")
        return "Error"


def find_and_add_roles(company_id, career_page_url):
    # Scrape the roles from career_page_url
    # For each role, populate the following variables: role_title, role_link, salary, score
    # Then, use the add_role_data function from supabase_service.py to add the role to Supabase
    pass