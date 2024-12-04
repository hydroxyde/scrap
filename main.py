import requests
from bs4 import BeautifulSoup
import csv
import time
import random

from dotenv import load_dotenv
import os

load_dotenv()

# Base URLs
base_url = os.getenv('BASE_URL')
actor_base_url = os.getenv('ACTOR_BASE_URL')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_actor_links(page_url):
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    actor_links = []
    for link in soup.find_all('a', href=True):
        if "/organizations/" in link['href']:
            actor_links.append(link['href'])
    
    return actor_links

def get_email_from_actor_page(actor_url):
    response = requests.get(actor_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    email_tag = soup.find('a', href=lambda href: href and "mailto:" in href)
    if email_tag:
        email = email_tag['href'].replace("mailto:", "").strip()
        if email:
            return email
    return None

def scrape_bioalps():
    with open("bioalps_emails.csv", 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Actor Name", "Email"]) 
        
        actor_links = get_actor_links(base_url)
        for actor_link in actor_links:
            actor_name = actor_link.split("/")[-2]  
            actor_url = f"{actor_base_url}{actor_name}/"
            
            email = get_email_from_actor_page(actor_url)
            if email:  # Only write if an email is found
                print("je print: ", [actor_name, email])
                csvwriter.writerow([actor_name, email])
            
            time.sleep(random.randint(20,100)/100)  # Be polite to the server

# Run the scraper
scrape_bioalps()