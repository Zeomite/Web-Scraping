# B2B Events Scraper

## Description
This script scrapes data for top five B2B events from their respective websites and compiles the data into JSON and CSV formats.

## Prerequisites
- Python 3.x
- `requests` library
- `beautifulsoup4` library

## How to Run
1. Clone this repository.
2. Install the required libraries using:
   ```
   pip install requests beautifulsoup4
   ```
3. Run the script:
   ```
   python main.py
   ```
4. The output files `b2b_events.json` and `b2b_events.csv` will be generated in the current directory.

## Data Collected
- Event Name
- Event Date(s)
- Location
- Website URL
- Description
- Key Speakers
- Agenda/Schedule
- Registration Details
- Pricing
- Categories
- Audience type
