import requests
from bs4 import BeautifulSoup
import re
import argparse
import json

def extract_int_from_string(input_string):
    # Use a regular expression to find the number in the string
    match = re.search(r'\d[\d,]*', input_string)
    if match:
        # Remove commas and convert to integer
        number = int(match.group().replace(',', ''))
        return number
    return None


def name_to_id(artist_name):
    with open("../data/artist_db.json", 'r') as file:
        artist_dict = json.load(file)
    try:
        artist_id  = artist_dict[artist_name]
        return artist_id
    except KeyError:
        raise KeyError(f"Artist '{artist_name}' not in database")



def get_spotify_listeners(artist_name):
    
    artist_id = name_to_id(artist_name)
    
    # Get artist page from Spotify
    artist_url = f"https://open.spotify.com/artist/{artist_id}"
    response = requests.get(artist_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch artist page for {artist_name}. Status code: {response.status_code}")
    
    # Parse the artist's page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the monthly listeners
    monthly_listeners = soup.find('div', {'data-testid': 'monthly-listeners-label'}).text
    
    monthly_listeners = extract_int_from_string(monthly_listeners)
    
    if not monthly_listeners:
        print(f"Monthly listeners not found for {artist_name}.")
        return None
    
    return monthly_listeners

def main():
    parser = argparse.ArgumentParser(description='Get monthly spotify listeners for an artist')
    parser.add_argument('artist_name', type=str, help='Find the monthly listeners for this artist')
    
    args = parser.parse_args()
    
    try:
        result = get_spotify_listeners(args.artist_name)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()