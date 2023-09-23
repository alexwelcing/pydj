from bs4 import BeautifulSoup
from googlesearch import search
import requests
import re
import logging
from .supabase_service import add_role_data

logger = logging.getLogger(__name__)

keywords = [
    'Product Management', 'Customer Advocacy', 'User Research and Insights',
    'Software', 'Development', 'Strategic', 'Roadmaps',
    'Leadership', 'GTM Strategy', 'Technical', 'Innovation',
    'AI', 'NLP', 'Advertising', 'Marketing', 'Developer'
]

def google_search_and_scrape(base_url):
    try:
        query = f"site:{base_url} careers OR jobs OR professionals OR 'Work with Us'"
        search_results = search(query, num=10, stop=10, pause=2.0)
        careers = []

        for url in search_results:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            appealing_jobs = soup.find_all(text=re.compile('|'.join(keywords), re.IGNORECASE))

            for job in appealing_jobs:
                if job.parent.name in ['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span']:
                    job_text = job.lower()
                    careers.append(job_text)

        return careers

    except Exception as e:
        logger.error(f"Error in google_search_and_scrape: {e}")
        return []

def find_and_add_roles_from_dives(company_id, base_url):
    try:
        careers = google_search_and_scrape(base_url)

        for career in careers:
            role_title = career
            role_link = None  # For now, as extracting exact link for each job is complex
            salary_match = re.search(r'\$(\d{3},\d{3})\+', career)
            salary = salary_match.group(0) if salary_match else None
            score = 5 if salary and int(salary_match.group(1).replace(',', '')) >= 180000 else 1
            
            add_role_data(company_id, role_title, role_link, salary, score)

    except Exception as e:
        logger.error(f"Error in find_and_add_roles_from_dives: {e}")
