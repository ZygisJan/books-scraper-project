# Books Scraper Project

This Python project scrapes book data from the website "Knygos.lt" by category and saves the data into JSON files.

# Features

- Scrapes books from multiple categories defined in the config.ini file
- Saves book data into separate JSON files for each category
- Handles pagination to scrape multiple pages in a category
- Extracts book titles, authors, publication years, and prices
- Logs errors and information into a log file (main.log)

# Installation

1. Clone the repository and navigate to the project directory:

   ```bash
git clone https://github.com/your-username/Books-project.git 
cd Books-project

2. Install the required dependencies:

pip install -r requirements.txt

3. Modify config.ini to set up scraping options like category URLs and pagination settings.

# Requirements
The project uses the following Python packages:

- requests
- beautifulsoup4
- configparser
- logging
- urllib.parse

# Configuration
The config.ini file contains the settings for scraping:

url: The starting URL of the category to scrape.
book_selector: The CSS selector for book links on the category page.
next_button_selector: The CSS selector for the next page button.
wait_time: Time to wait between page requests (in seconds).
max_pages: Maximum number of pages to scrape.

# Logs
Errors and logs are stored in the main.log file.
This file tracks the scraping process, including when the script encounters an issue or successfully processes a page.
