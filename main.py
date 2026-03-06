from Scraper import *
from MessageBot import MessageBot
from Database import Database
import os

def main():

    # Fetch all jobs
    jobFinder = JobFinder("Israel", ["Data Engineer"])
    jobs = jobFinder.fetch_linkedin_jobs()
    
    # Get bot token and chat id
    token = os.environ["TELEGRAM_BOT_TOKEN_STUDENT_JOBS"]
    chat_id = os.environ["TELEGRAM_CHAT_ID_STUDENT_JOBS"]
    bot = MessageBot(token, chat_id)
    
    # Get db username and password
    username = os.environ["MONGODB_USERNAME"]
    password = os.environ["MONGODB_PASSWORD"]
    url = f"mongodb+srv://{username}:{password}@student-jobs.fw1npmz.mongodb.net/?appName=student-jobs"
    db = Database(url)
    
    for job in jobs:
        result = db.list_jobs(job)
        if result: 
            bot.send_message(str(job))
            print(job)

main()