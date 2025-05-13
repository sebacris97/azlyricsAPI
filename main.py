
import json
from fastapi import FastAPI, Path, HTTPException
import requests
from urllib.parse import unquote
from fastapi.responses import JSONResponse
import os
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS
from fake_useragent import UserAgent
import random
import httpx
from fastapi.middleware.cors import CORSMiddleware
from azlyricsbrave import get_brave_lyrics

ua = UserAgent()
HEADERS = {'User-Agent': ua.random,
           'Accept-Encoding': 'gzip, deflate',
           'Accept': '*/*',
           'Connection': 'keep-alive'
           }

app = FastAPI()



# Allow requests from your frontend origin
origins = [
    "https://teal-bombolone-e98a8f.netlify.app/"  # or wherever your frontend is hosted
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extern_requestScrA(url):
    TOKEN = os.environ.get('TOKEN')
    SCRAP_URL = os.environ.get('S_URL')
    PAYLOAD = { 'api_key': TOKEN, 'url': url,
                'follow_redirect': 'true', 'retry_404': 'true' }
    return requests.get(SCRAP_URL, params=PAYLOAD)


def extern_request(url):
    SCRAP_URL = "https://azlyrics.com"
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    gateway = ApiGateway(SCRAP_URL,
                         access_key_id = AWS_ACCESS_KEY_ID,
                         access_key_secret = AWS_SECRET_ACCESS_KEY,
                         regions=EXTRA_REGIONS
                         )
    gateway.start()
    session = requests.Session()
    session.mount(SCRAP_URL, gateway)
    return session.get(url,headers=HEADERS)
    #gateway.shutdown() 



@app.get("/")
async def root():
    return "main page"


@app.get("/api/get-lyrics/{artist_name}/{song_name}/")
def read_lyrics_extern2(artist_name: str, song_name: str):
    data = get_brave_lyrics(artist=unquote(artist_name).lower(),
                        song=unquote(song_name).lower(),
                        request=extern_requestScrA
                        )
    if not data:
        raise HTTPException(status_code=404, detail="Lyrics not found")
    return data



@app.get("/get-lyrics/{artist_name}/{song_name}/")
def read_lyrics_extern(artist_name: str, song_name: str):
    data = get_brave_lyrics(artist_name=unquote(artist_name).lower(),
                        song_name=unquote(song_name).lower(),
                        request=extern_request
                        )
    if not data:
        raise HTTPException(status_code=404, detail="Lyrics not found")
    data['lyrics'] = data['lyrics'].encode('ISO-8859-1')
    return data




@app.get("/local/get-lyrics/{artist_name}/{song_name}")
def read_lyrics(artist_name: str, song_name: str):
    data = get_brave_lyrics(artist_name=unquote(artist_name).lower(),
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
