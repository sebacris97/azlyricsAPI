from fastapi import FastAPI
from azlyrics_scraper import get_lyrics
import requests
from urllib.parse import unquote

app = FastAPI()

def extern_request(url):
    TOKEN = "MY_SECRET_TOKEN"
    SCRAP_URL = "https://my-scraper-api-url.com/"
    PAYLOAD = { 'api_key': TOKEN, 'url': url,
                'follow_redirect': 'true', 'retry_404': 'true' }
    return requests.get(SCRAP_URL, params=PAYLOAD)

@app.get("/")
async def root(artist_name,song_name):
    print(unquote(artist_name))
    print(unquote(song_name))
    lyrics = get_lyrics(
                    artist_name = artist_name,
                    song_name = song_name,
                    #request = extern_request,
                    #save_json = True,
                    return_json = True
                    )
    return lyrics

@app.get("/{artist_name}/{song_name}")
async def get_lyrics_view(artist_name,song_name):
    print(unquote(artist_name))
    print(unquote(song_name))
    lyrics = get_lyrics(
                    artist_name = artist_name,
                    song_name = song_name,
                    #request = extern_request,
                    #save_json = True,
                    return_json = True
                    )
    return lyrics
