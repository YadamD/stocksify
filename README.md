# stocksify
Spotify artist stocks

### Setup conda environment:
`conda create -n myenv anaconda`

`conda activate myenv`

`pip install -r requirements.txt`

### Usage:
- Navigate to directory
- `python get_monthly_listeners.py "ArtistName"`

### Notes

Only artists in `artist_db.json` can be searched. To add artists, go to the desired artist's page on Spotify, click the 3 dots -> Share -> Copy link to artist. Cut the ID of the artist, and add it to the `artist_db.json` with the artist name.


![image](https://github.com/user-attachments/assets/bed356c9-3c6a-4e3b-8c53-cfb1715f67b2)
