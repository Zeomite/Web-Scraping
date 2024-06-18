import requests
from bs4 import BeautifulSoup
import json
import csv

# List of B2B event URLs 
event_urls = [
    "https://www.b2bmarketing.net/events/",
    "https://www.dmexco.com",
    "https://www.inbound.com",
    "https://www.saastrannual.com",
    "https://events.marketingprofs.com"
]


def extract_audience_type(text):
    keywords = ["who should attend", "target audience", "for", "attendees"]
    audience = "N/A"
    for keyword in keywords:
        if keyword in text.lower():
            start_idx = text.lower().find(keyword)
            end_idx = start_idx + 200 
            audience = text[start_idx:end_idx]
            break
    return audience

def scrape_event_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    event_data = {}
    event_data['Website URL'] = url
    event_data['Event Name'] = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
    event_data['Description'] = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'N/A'
    event_data['Event Date(s)'] = soup.find('time').text.strip() if soup.find('time') else 'N/A'
    event_data['Location'] = soup.find('div', {'class': 'location'}).text.strip() if soup.find('div', {'class': 'location'}) else 'N/A'
    event_data['Key Speakers'] = ', '.join([speaker.text.strip() for speaker in soup.find_all('h3', class_='speaker-name')])
    event_data['Agenda/Schedule'] = ' | '.join([agenda.text.strip() for agenda in soup.find_all('div', class_='agenda-item')])
    event_data['Registration Details'] = soup.find('a', {'class': 'register-button'})['href'] if soup.find('a', {'class': 'register-button'}) else 'N/A'
    event_data['Pricing'] = soup.find('div', {'class': 'pricing'}).text.strip() if soup.find('div', {'class': 'pricing'}) else 'N/A'
    event_data['Categories'] = ', '.join([category.text.strip() for category in soup.find_all('div', class_='category')])
    audience_section = soup.find('div', {'class': 'audience-section'}) if soup.find('div', {'class': 'audience-section'}) else 'N/A'
    event_data['Audience type'] = extract_audience_type(audience_section.text) if audience_section != 'N/A' else 'N/A'
    
    return event_data


all_event_data = []

# Scrape data for each event
for url in event_urls:
    event_data = scrape_event_data(url)
    all_event_data.append(event_data)

# Save data to JSON file
with open('b2b_events.json', 'w') as json_file:
    json.dump(all_event_data, json_file, indent=4)

# Save data to CSV file
with open('b2b_events.csv', 'w', newline='') as csv_file:
    fieldnames = ['Event Name', 'Event Date(s)', 'Location', 'Website URL', 'Description', 'Key Speakers', 'Agenda/Schedule', 'Registration Details', 'Pricing', 'Categories', 'Audience type']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for event in all_event_data:
        writer.writerow(event)

print("Scraping Completed!")
