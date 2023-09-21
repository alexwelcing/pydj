# dives.py
from bs4 import BeautifulSoup
from googlesearch import search
import requests
import re
import logging
from .supabase_service import update_supabase_data

logger = logging.getLogger(__name__)

keywords = [
    'Product Management', 'Customer Advocacy', 'User Research and Insights',
    'Software', 'Development', 'Strategic', 'Roadmaps',
    'Leadership', 'GTM Strategy', 'Technical', 'Innovation',
    'AI', 'NLP', 'Advertising', 'Marketing', 'Developer'
]

def google_search_and_scrape(base_url, row):
    try:
        query = f"site:{base_url} careers OR jobs OR professionals OR 'Work with Us'"
        search_results = search(query, num=10, stop=10, pause=2.0)
        careers = []
        roles_estimate = 0

        for url in search_results:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            appealing_jobs = soup.find_all('div', {'class': 'job-listing'})

            for job in appealing_jobs:
                job_text = job.text.lower()
                if any(keyword.lower() in job_text for keyword in keywords):
                    careers.append(job.text)

                salary_match = re.search(r'\$(\d{3},\d{3})\+', job_text)
                if salary_match:
                    salary = int(salary_match.group(1).replace(',', ''))
                    if salary >= 180000:
                        roles_estimate += 5
                    else:
                        roles_estimate += 1
                else:
                    roles_estimate += 1

        row['careers'] = careers
        row['roles'] = roles_estimate
        update_supabase_data([row])

    except Exception as e:
        logger.error(f"Error in google_search_and_scrape: {e}")
