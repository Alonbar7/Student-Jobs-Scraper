from Scraper import *
from MessageBot import MessageBot

import os
from dotenv import load_dotenv

def main():

    # Fetch all jobs
    jobFinder = JobFinder("Israel", ["Data Engineer"])
    jobs = jobFinder.fetch_linkedin_jobs()
    
    # Get bot token and chat id
    load_dotenv()
    token = os.environ["TELEGRAM_BOT_TOKEN_STUDENT_JOBS"]
    chat_id = os.environ["TELEGRAM_CHAT_ID_STUDENT_JOBS"]
    bot = MessageBot(token, chat_id)
    
    for job in jobs:
        bot.send_message(str(job))
        print(job)

main()