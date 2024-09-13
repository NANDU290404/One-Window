import requests
from bs4 import BeautifulSoup
import time
import json

# Main URL and base URL
mainUrl = 'https://www.4icu.org/de/universities/'
baseUrl = 'https://www.4icu.org'

# Fetch the main page
response = requests.get(mainUrl)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

# Extract state links
tables = soup.find('table', class_='table')
stateLinks = []

for aTag in tables.find_all('a', href=True):
    stateName = aTag.text.strip()
    stateUrl = baseUrl + aTag['href']
    stateLinks.append({'state name': stateName, 'state url': stateUrl})

# Display the states and URLs
for state in stateLinks:
    print(f"state: {state['state name']}, URL: {state['state url']}")
print(f"Total {len(stateLinks)} states")

# Extract university links from each state
stateUniversities = []
for state in stateLinks:
    url = state['state url']
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    uni_table = soup.find('tbody')
    universityLinks = []

    for aTag in uni_table.find_all('a', href=True):
        if aTag['href'] == '/about/add.htm':
            continue
        uniUrl = baseUrl + aTag['href']
        universityLinks.append(uniUrl)
    stateUniversities.append({'state': state['state name'], 'universityLinks': universityLinks})

# Function to determine social media type
def determine_media_type(url):
    if 'facebook.com' in url:
        return 'facebook'
    elif 'instagram.com' in url:
        return 'instagram'
    elif 'twitter.com' in url:
        return 'twitter'
    elif 'linkedin.com' in url:
        return 'linkedin'
    elif 'youtube.com' in url:
        return 'youtube'
    else:
        return 'unknown'

# Extract details from each university page
universities = []
for university in stateUniversities:
    stateName = university['state']
    for uniUrl in university['universityLinks']:
        response = requests.get(uniUrl)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        # Extract information with safety checks for missing elements
        logo = soup.find('img', attrs={"itemprop": "logo"})
        uniName = soup.find('h1', attrs={"itemprop": "name"})
        cityName = soup.find('span', attrs={"itemprop": "addressLocality"})
        type = soup.find('p', class_='lead').find('strong')
        foundedYear = soup.find('table', class_='table borderless')
        socialLinks = soup.find('div', attrs={"id": "social-media"})
        uniLink = soup.find('a', attrs={"itemprop": "url"})

        # Continue only if essential data exists
        if not uniName or not cityName or not type or not foundedYear or not uniLink:
            continue

        foundedYear = foundedYear.find('span', attrs={"itemprop": "foundingDate"})

        # Parse social links
        socialUrls = []
        if socialLinks:
            socialLinks = socialLinks.find_all('a', attrs={"itemprop": "sameAs"})
            for url in socialLinks:
                socialUrls.append({'media': determine_media_type(url['href']), 'link': url['href']})

        # Map social media URLs
        social_media_map = {
            'facebook': '',
            'twitter': '',
            'instagram': '',
            'linkedin': '',
            'youtube': ''
        }
        for social_url in socialUrls:
            url = social_url['link']
            if 'facebook.com' in url:
                social_media_map['facebook'] = url
            elif 'twitter.com' in url:
                social_media_map['twitter'] = url
            elif 'instagram.com' in url:
                social_media_map['instagram'] = url
            elif 'linkedin.com' in url:
                social_media_map['linkedin'] = url
            elif 'youtube.com' in url:
                social_media_map['youtube'] = url

        # Create entry
        entry = {
            "name": uniName.text.strip(),
            "location": {
                "country": "Germany",
                "state": stateName,
                "city": cityName.text.strip()
            },
            "logoSrc": logo['src'] if logo else '',
            "type": type.text.strip(),
            "establishedYear": foundedYear.text.strip() if foundedYear else '',
            "contact": {
                "facebook": social_media_map['facebook'],
                "twitter": social_media_map['twitter'],
                "instagram": social_media_map['instagram'],
                "officialWebsite": str(uniLink['href']),
                "linkedin": social_media_map['linkedin'],
                "youtube": social_media_map['youtube']
            }
        }

        universities.append(entry)
        print(f"Processed {entry['name']}")

        # Adding delay to avoid overwhelming the server
        time.sleep(1)

# Save to JSON file
with open('universities.json', 'w', encoding='utf-8') as f:
    json.dump(universities, f, ensure_ascii=False, indent=4)

print(f"Data saved to universities.json with {len(universities)} entries.")
