# stocksify
Spotify artist stocks

### Setup conda environment:
`conda create -n myenv anaconda`

`conda activate myenv`

`pip install -r requirements.txt`

### Useage:
- Navigate to directory
- `python get_monthly_listeners.py "ArtistName"`

### Notes

Only artists in `artist_db.json` can be searched. To add artists, go to the desired artist's page on Spotify, click the 3 dots -> Share -> Copy link to artist. Cut the ID of the artist, and add it to the `artist_db.json` with the artist name.
