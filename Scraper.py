import requests
from bs4 import BeautifulSoup
import time
import random

# Job container
class Job:
    def __init__(self, title, company, link):
        self.title = title
        self.company = company
        self.link = link

    def __str__(self):
        msg = f"Title: {self.title}\n"
        msg += f"Company: {self.company}\n"
        msg += f"Link: {self.link}\n"
        return msg

# Job API Request & Proccessing
class JobFinder:
    
    def __init__(self, location="Israel", positions=["Date Engineer"]):
        self.location = location
        self.positions = positions

    def construct_link(self):
        # Base url
        url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords="
        
        # Add positions
        if not self.types:
            return None

        for position in self.positions:
            updated = position.replace(" ", "+")
            url += updated
        
        # Add locations
        url += f"&location={self.location}"
        url += "&f_E=1,2&f_JT=P,I&start=0"

        self.url = url

        return url

    def fetch_linkedin_jobs(self):
        # Url link specified for my needs
        # url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data+Engineer&location=Israel&f_E=1,2&f_JT=P,I&start=0"
        self.construct_link()

        # Browswer agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            # Request Guest API
            response = requests.get(self.url, headers=headers)

            if response.status_code != 200:
                print(f"API request failed. Status code: {response.status_code}")
                return None
            else:
                print("API Request Worked!")

            # Proccessing the information
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get job tabs from the result
            job_cards = soup.find_all('div', class_='base-card')        
            if not job_cards:
                job_cards = soup.find_all('li')

            print(f"Found {len(job_cards)} jobs.")
            print("-" * 40)

            jobs = []

            # Get elements
            for index, card in enumerate(job_cards, start=1):
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    company = company_elem.get_text(strip=True) if company_elem else "N/A"
                    
                    link_elem = card.find('a', class_='base-card__full-link')
                    job_link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else "No Link"
                    
                    clean_link = job_link.split('?')[0]
                    
                    job = Job(title, company, clean_link)
                    jobs.append(job)

                except Exception as e:
                    print(e)
                    return jobs if jobs else None
        except Exception:
            print("Failuer Exceuting")
            return None
        
        return jobs

jobFinder = JobFinder()
jobs = jobFinder.fetch_linkedin_jobs()
for job in jobs:
    print(job)