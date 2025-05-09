
import json
from fastapi import FastAPI, Path, HTTPException
from azlyrics_scraper import get_lyrics
import requests
from urllib.parse import unquote
from fastapi.responses import JSONResponse
import os
from requests_ip_rotator import ApiGateway

app = FastAPI()

"""
def extern_request2(url):
    TOKEN = os.environ.get('TOKEN')
    SCRAP_URL = os.environ.get('S_URL')
    PAYLOAD = { 'api_key': TOKEN, 'url': url,
                'follow_redirect': 'true', 'retry_404': 'true' }
    return requests.get(SCRAP_URL, params=PAYLOAD)
"""


SCRAP_URL = "https://azlyrics.com"
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
def extern_request(url):
    with ApiGateway(SCRAP_URL,
                    access_key_id = AWS_ACCESS_KEY_ID,
                    access_key_secret = AWS_SECRET_ACCESS_KEY) as g:
        session = requests.Session()
        session.mount("https://site.com", g)
        return session.get(url)


@app.get("/")
async def root():
    return "main page"


@app.get("/get-lyrics/{artist_name}/{song_name}/")
def read_lyrics_extern(artist_name: str, song_name: str):
    data = get_lyrics(artist_name=unquote(artist_name).lower(),
                        song_name=unquote(song_name).lower(),
                        request=extern_request
                        )
    if not data:
        raise HTTPException(status_code=404, detail="Lyrics not found")
    return data


@app.get("/local/get-lyrics/{artist_name}/{song_name}")
def read_lyrics(artist_name: str, song_name: str):
    data = get_lyrics(artist_name=unquote(artist_name).lower(),
                        song_name=unquote(song_name).lower(),
                        )
    if not data:
        raise HTTPException(status_code=404, detail="Lyrics not found")
    data['lyrics'] = data['lyrics'].encode('ISO-8859-1')
    return data


"""
@app.get("/get-lyrics/{artist_name}/{song_name}")
async def get_lyrics_view(artist_name:
                          str = Path(..., description="Artist name to be rerieved."),
                          song_name:
                          str = Path(..., description="Song name to be rerieved."),):
    lyrics = get_lyrics(
                    artist_name = unquote(artist_name),
                    song_name = unquote(song_name),
                    #request = extern_request,
                    #save_json = True,
                    #return_json = True
                    )
    return JSONResponse(content=
                        {"artist": artist_name,
                         "song": song_name,
                         "lyrics": lyrics
                        })
"""
