from Scraper import *
from MessageBot import send_message

def main():

    jobFinder = JobFinder("Israel", ["Data Engineer"])
    jobs = jobFinder.fetch_linkedin_jobs()
    for job in jobs:
        send_message(str(job))
        print(job)

main()