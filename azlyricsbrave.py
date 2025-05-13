import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
import re

SEARCH_SITE = "azlyrics.com"
BRAVE_URL = 'https://api.search.brave.com/res/v1/web/search?q='

UA = UserAgent()

DEFAULT_HEADERS = {
                  'User-Agent':UA.random,
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


def brave_search(artist, song, request=default_request):
    artist = re.sub(' +', ' ', artist).replace(' ','+')
    song = re.sub(' +', ' ', song).replace(' ','+')
    BRAVE_FINAL_URL = f'{BRAVE_URL}{artist}+{song}+site%3A{SEARCH_SITE}&source=web'
    return request(BRAVE_FINAL_URL, headers=BRAVE_HEADERS, params=BRAVE_PARAMS).json()


def scraped_song_lyrics(response):
    soup = BeautifulSoup(response.text,'html.parser')
    return soup.find_all("div")[24].text.replace('\r','')


def clean_data(response):
    url = response['web']['results'][0]['url']
    artist = response['web']['results'][0]['title'].split(' - ')[0]
    song = response['web']['results'][0]['title'].split(' - ')[1].split(' Lyrics')[0]
    return artist, song, url


def get_brave_lyrics(artist='',song='',request=default_request):
    search_response = brave_search(artist,song)
    artist, song, lyrics_url = clean_data(search_response)
    print(artist,' ',song,' ',lyrics_url)
    lyrics_response = request(lyrics_url)
    print(lyrics_response.text)
    lyrics = scraped_song_lyrics(lyrics_response)
    return {'artist':artist,'song':song,'lyrics':lyrics}

