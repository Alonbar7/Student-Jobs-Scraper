from Scraper import *

def main():

    jobFinder = JobFinder("Israel", ["Data Engineer"])
    jobs = jobFinder.fetch_linkedin_jobs()
    for job in jobs:
        print(job)

main()