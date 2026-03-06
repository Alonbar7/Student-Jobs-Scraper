# Student Jobs Scraper and ETL Pipeline
An automated Data Pipeline built in Python that extracts LinkedIn job postings, filters relevant student and junior positions, stores them in a NoSQL database, and triggers real-time notifications.

## Architecture

The project is structured as a lightweight ETL (Extract, Transform, Load) pipeline:

* **Extract (Web Scraping):** Uses `requests` and `BeautifulSoup4` to query the LinkedIn Guest API. Bypasses pagination limits to extract complete job listings (Title, Company, Link, and Job ID).
* **Transform (Data Cleaning):** Implements dynamic filtering using a custom Blacklist to remove irrelevant jobs, spam listings (e.g., "Online Data Analyst"), and extracts natural keys (LinkedIn Job IDs) using Regular Expressions (`re`).
* **Load (Database):** Connects to **MongoDB Atlas** using `pymongo`. Utilizes `Upsert` logic and unique indexing to ensure only new, non-duplicate jobs are inserted into the collection.
* **Alerting:** Integrates with the **Telegram Bot API** to push real-time notifications straight to a mobile device whenever a new, relevant job is added to the database.
* **Automation (CI/CD):** Fully automated using **GitHub Actions**. A Cron Job runs the script twice a day on an ephemeral Ubuntu server, utilizing GitHub Secrets to securely manage database credentials and bot tokens.
## Technical Specifications

- **Smart Pagination:** Automatically navigates through LinkedIn's API pages until all relevant jobs are fetched.
- **Duplicate Prevention:** MongoDB handles data integrity, ensuring you never get notified about the same job twice.
- **Targeted Search:** Configured specifically to hunt for Data Engineering, Backend, and Python student roles in Israel.
- **Serverless Automation:** Runs 100% in the cloud via GitHub Actions, requiring no local machine uptime.
