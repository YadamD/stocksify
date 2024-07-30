import json
import pandas as pd
from get_monthly_listeners import get_spotify_listeners
from datetime import datetime

def add_listeners_to_csv(json_file='../data/artist_db.json', csv_file='../data/listeners_data.csv'):
    # Load the dictionary from the JSON file
    with open(json_file, 'r') as file:
        artist_dict = json.load(file)
    
    # Read the existing CSV file into a DataFrame
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        # If the file does not exist, create an empty DataFrame with the correct columns
        df = pd.DataFrame(columns=['Date'] + list(artist_dict.keys()))

    
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Check if the current date is already in the DataFrame
    if current_date in df['Date'].values:
        if set(df.columns) == set(list(artist_dict.keys()) + ['Date']):
            print("Stock data up to date")
            return
        
        df = df[df['Date'] != current_date]
    
        # Check for missing artist columns and add them with NaN values
    for artist_name in artist_dict.keys():
        if artist_name not in df.columns:
            print(f"Adding new artist {artist_name} to data and resetting today's values")
            df[artist_name] = pd.Series([float('nan')] * len(df))
    
    # Create a dictionary to hold the new row of data
    new_row = {'Date': current_date}

    # Iterate through the dictionary keys
    for artist_name in artist_dict.keys():
        # Call the get_spotify_listeners function and store the result
        listeners = get_spotify_listeners(artist_name)
        new_row[artist_name] = listeners
    
    # Append the new row to the DataFrame
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    

    # Save the updated DataFrame to the CSV file
    df.to_csv(csv_file, index=False)

def main():
    add_listeners_to_csv()

if __name__ == '__main__':
    main()