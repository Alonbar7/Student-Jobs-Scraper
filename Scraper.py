import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random
import re

# Job container
class Job:
    def __init__(self, job_id, title, company, link):
        self.id = job_id
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
    
    def __init__(self, location="Israel", positions = ["Date Engineer"], blacklist = []):
        self.location = location
        self.positions = positions
        self.blacklist = blacklist

    def construct_link(self, start = 0):        
        if not self.positions:
            return None

        # Create search query
        search = " OR ".join(self.positions)
        encoded_search = urllib.parse.quote(search)

        # Construct url
        # url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data+Engineer&location=Israel&f_E=1,2&f_JT=P,I&start=0"
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={encoded_search}&location={self.location}&f_E=1,2&f_JT=P,I&sortBy=DD&start={start}"
        print(url)
        return url

    def fetch_linkedin_jobs(self):
        # Url page counter
        page_number = 0
        job_start_index = 0
        
        # Jobs holder
        self.jobs = []
        
        # Browswer agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        while True:
            try:
                # Create url
                url = self.construct_link(job_start_index)
                
                # Request Guest API
                response = requests.get(url, headers=headers)

                if response.status_code != 200:
                    return None

                # Proccessing the information
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get job tabs from the result
                job_cards = soup.find_all('div', class_='base-card')        
                if not job_cards:
                    job_cards = soup.find_all('li')
                    
                # Break loop if reached an empty page
                if not job_cards:
                    break

                # Get elements
                for index, card in enumerate(job_cards, start=1):
                    try:
                        title_elem = card.find('h3', class_='base-search-card__title')
                        title = title_elem.get_text(strip=True) if title_elem else "N/A"
                        
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        company = company_elem.get_text(strip=True) if company_elem else "N/A"
                        
                        # Filter blacklist jobs
                        title_lower = title.lower()
                        company_lower = company.lower()
                        if any(banned_word.lower() in title_lower or banned_word.lower() in company_lower for banned_word in self.blacklist):
                            print(f"Filtered by blacklist: {title} from {company}")
                            continue
                        
                        link_elem = card.find('a', class_='base-card__full-link')
                        job_link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else "No Link"
                        
                        clean_link = job_link.split('?')[0]
                        
                        regex_id = re.search(r'\d{9,10}', clean_link)
                        if not regex_id: continue
                        job_id = regex_id.group(0)
                        
                        job = Job(job_id, title, company, clean_link)
                        self.jobs.append(job)

                    except Exception as e:
                        print(e)
                        return self.jobs if self.jobs else None
                    
                print(f'Scanned page {page_number}, {len(job_cards)} found.')
                
                # Go to the next page
                job_start_index += len(job_cards)
                page_number += 1
                
                # Rest to counter block
                time.sleep(random.uniform(2.0, 4.0))
            except Exception:
                print("Failuer Exceuting")
                return None
        
        return self.jobs
    