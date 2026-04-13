from Scraper import *
from MessageBot import MessageBot
from Database import Database
import os

def main():

    # Fetch all jobs
    intrests = ["Data Engineering Student", "Student Data Engineer", "Python Student"]
    blacklist = ["Electrical"]
    jobFinder = JobFinder("Israel", intrests, blacklist)
    jobs = jobFinder.fetch_linkedin_jobs()
    
    # Get bot token and chat id
    token = os.environ["TELEGRAM_BOT_TOKEN_STUDENT_JOBS"]
    chat_id = os.environ["TELEGRAM_CHAT_ID_STUDENT_JOBS"]
    bot = MessageBot(token, chat_id)
    
    # Get db username and password
    username = os.environ["MONGODB_USERNAME"]
    password = os.environ["MONGODB_PASSWORD"]
    url = f"mongodb+srv://{username}:{password}@student-jobs.fwwrw0y.mongodb.net/?appName=student-jobs"
    db = Database(url)
    
    new_jobs = 0
    for job in jobs:
        result = db.list_jobs(job)
        if result: 
            new_jobs += 1
            bot.send_message(str(job))
            print(job)
        
    print(f"Added {new_jobs} new jobs.")

main()