import requests
from bs4 import BeautifulSoup
import os
import re


LY = "lyrics.com"
AZ = "azlyrics.com"
BRAVE_URL = 'https://api.search.brave.com/res/v1/web/search?q='


DEFAULT_HEADERS = {
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept': '*/*',
                  'Connection': 'keep-alive'
                  }

BRAVE_HEADERS = {
                'Accept':'application/json',
                'Accept-Encoding':'gzip',
                'X-Subscription-Token': os.environ.get('BRAVE_TOKEN')
                }

BRAVE_PARAMS = {
                'count':1
               }


def default_request(url, headers=DEFAULT_HEADERS, params={}):
     return requests.get(url, headers=headers, params=params)


def brave_search(artist, song, SEARCH_SITE=LY, request=default_request):
    artist = re.sub(' +', ' ', artist).replace(' ','+')
    song = re.sub(' +', ' ', song).replace(' ','+')
    BRAVE_FINAL_URL = f'{BRAVE_URL}{artist}+{song}+site%3A{SEARCH_SITE}&source=web'
    search = request(BRAVE_FINAL_URL, headers=BRAVE_HEADERS, params=BRAVE_PARAMS).json()
    return search


def scraped_song_lyrics(response,SEARCH_SITE):
    soup = BeautifulSoup(response.text,'html.parser')
    if SEARCH_SITE == LY:
        return soup.find(id="lyric-body-text").text
    return soup.find_all("div")[24].text.replace('\r','')

def clean_data(response, song):
    first_result = response['web']['results'][0]
    title = first_result['title'].split(' - ')
    song = title[1].split(' Lyrics')[0]
    artist = title[0]
    url = first_result['url']
    return artist, song, url


def get_brave_lyrics(artist='',song='',request=default_request,SEARCH_SITE=LY):
    search_response = brave_search(artist,song,SEARCH_SITE)
    artist, song, lyrics_url = clean_data(search_response, song)
    lyrics_response = request(lyrics_url)
    try:
        lyrics = scraped_song_lyrics(lyrics_response,SEARCH_SITE)
    except:
        return get_brave_lyrics(artist,song,request,SEARCH_SITE=AZ)
    return {'artist':artist,'song':song,'lyrics':lyrics}



