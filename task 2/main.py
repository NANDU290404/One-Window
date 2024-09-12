import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://www.4icu.org/de/universities/'

def extract_university_info(university):
    """Extract information from a university block."""
    try:
        # Example structure, adjust as per actual HTML
        name_tag = university.find('h3')
        name = name_tag.text.strip() if name_tag else 'Unknown'

        logo_tag = university.find('img')
        logo_src = logo_tag['src'] if logo_tag else 'Unknown'

        # Adjusted for simplicity; the example HTML may not have 'type' and 'founded' tags
        # Adding dummy values if real data isn't found
        university_type = 'Unknown'
        founded_year = 'Unknown'

        # Assuming location details might not be in this HTML snippet
        country = 'Germany'
        state = 'Unknown'
        city = 'Unknown'

        phone_number = 'Unknown'

        social_media = {
            'facebook': 'Unknown',
            'twitter': 'Unknown',
            'instagram': 'Unknown',
            'linkedin': 'Unknown',
            'youtube': 'Unknown',
            'officialWebsite': 'Unknown',
        }

        return {
            'name': name,
            'location': {
                'country': country,
                'state': state,
                'city': city
            },
            'logoSrc': logo_src,
            'type': university_type.lower(),
            'establishedYear': founded_year,
            'contact': social_media
        }

    except Exception as e:
        print(f"Error extracting information: {e}")
        return None

def get_universities_data():
    """Fetch university data from the website."""
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Debugging output to inspect the HTML
        print(soup.prettify())

        universities_data = []

        # Placeholder for actual university blocks
        # You'll need to identify the correct class or structure for university items
        university_blocks = soup.find_all('div', class_='panel')

        if not university_blocks:
            print("No university blocks found. Check the HTML structure.")
            return []

        for block in university_blocks:
            university_info = extract_university_info(block)
            if university_info:
                universities_data.append(university_info)
            else:
                print("Failed to extract information from a block.")

        return universities_data

    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []

def main():
    data = get_universities_data()

    if data:
        with open('universities.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print("Data successfully written to universities.json")
    else:
        print("No data to write.")

if __name__ == "__main__":
    main()
