from fastapi import FastAPI, Path, HTTPException
from azlyrics_scraper import get_lyrics
import requests
from urllib.parse import unquote
from fastapi.responses import JSONResponse

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



app = FastAPI()

@app.get("/get-lyrics/{artist_name}/{song_name}")
def read_lyrics(artist_name: str, song_name: str):
    # Decodificar en caso de que venga con %20 u otros caracteres
    artist_name = unquote(artist_name)
    song_name = unquote(song_name)
    
    try:
        lyrics = get_lyrics(artist_name=artist_name, song_name=song_name)
        if not lyrics:
            raise HTTPException(status_code=404, detail="Lyrics not found")
        return {"artist": artist_name, "song": song_name, "lyrics": lyrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
