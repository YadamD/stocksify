# stocksify
Spotify artist stocks

## TODO
- [x] Add scheduled run to auto-log data every day!
  - Added with github actions    
- [ ] Add more artists - to add an artist, see **Notes**
- [ ] Check Vercel for deployment

### Setup conda environment:
`conda create -n myenv anaconda`

`conda activate myenv`

`pip install -r requirements.txt`

### Setup page requirements

- Make sure you have `npm` installed
- `npm install` when in the `stocksify_page/stocksify-page` project
- `npm run dev` to host the page locally

### Usage:
- Navigate to directory
- Get listeners for one artist: `python get_monthly_listeners.py "ArtistName"`
- Update stock history: `python update_stock_history.py`
  - This will add a new entry to CSV only if the current date is not included, and update today's entry if new artist is added 

### Notes

Only artists in `artist_db.json` can be searched. To add artists, go to the desired artist's page on Spotify, click the 3 dots -> Share -> Copy link to artist. Cut the ID of the artist, and add it to the `artist_db.json` with the artist name.

![image](https://github.com/user-attachments/assets/51e1580a-aae3-42fb-8590-30976e83294f)

