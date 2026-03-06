from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from Scraper import Job
import time
import os

class Database:
    
    def __init__(self, connection_url):
        self.url = connection_url
        self.connection = self._connect_to_mongo()

    # Connect to db
    def _connect_to_mongo(self):
        try:
            # Connect
            client = MongoClient(self.url)        
            db = client['jobs_db']        
            collection = db['linkedin_jobs']

            # Create index
            collection.create_index("job_id", unique=True)
            
            print("Connection to db worked")
            return collection
            
        except ConnectionFailure as e:
            print("Connection to db failed")
            return None

    # Create listing on db
    def _process_job_listing(self, job: Job):
        job_document = {
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "link": job.link,
            "scraped_at": time.time()
        }

        # Add it if its new
        result = self.connection.update_one(
            {"job_id": job.id},
            {"$setOnInsert": job_document},
            upsert=True
        )
        
        # Print result
        return True if result.upserted_id is not None else False
    
    # User function to add a job to db
    def list_jobs(self, job: Job):
        # Check if connection exists
        if self.connection is None:
            return False
        
        result = self._process_job_listing(job)
        return result
