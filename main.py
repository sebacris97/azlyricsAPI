from fastapi import FastAPI, Path
from azlyrics_scraper import get_lyrics
import requests
from urllib.parse import unquote

app = FastAPI()

async def extern_request(url):
    TOKEN = "MY_SECRET_TOKEN"
    SCRAP_URL = "https://my-scraper-api-url.com/"
    PAYLOAD = { 'api_key': TOKEN, 'url': url,
                'follow_redirect': 'true', 'retry_404': 'true' }
    return await requests.get(SCRAP_URL, params=PAYLOAD)

@app.get("/")
async def root():
    return "main page"

@app.get("/get-lyrics/{artist_name}/{song_name}")
async def get_lyrics_view(artist_name:
                          str = Path(..., description="Artist name to be rerieved."),
                          song_name:
                          str = Path(..., description="Song name to be rerieved."),):
    print(unquote(artist_name))
    print(unquote(song_name))
    lyrics = await get_lyrics(
                    artist_name = artist_name,
                    song_name = song_name,
                    #request = extern_request,
                    #save_json = True,
                    return_json = True
                    )
    return lyrics
