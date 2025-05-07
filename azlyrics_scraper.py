import requests
from bs4 import BeautifulSoup
import json
import os
from az_google_search import perform_search

BASE_URL = "https://www.azlyrics.com"

def search_key_like(dic, query):
    for key in dic.keys():
        if query.lower() in key.lower():
            return dic[key]
    return dic[query]


def cleaned_artist_name(artist):
    return ''.join(artist.split(' '))

def artist_url(artist):
    return f"{BASE_URL}/{artist[0]}/{cleaned_artist_name(artist)}.html"

def song_url(link):

    a = link.find('a').attrs['href']
    return link.find('a').attrs['href']

#sometimes the href is from an external azlyrics page
#cleaning the url avoids getting wrong links
def cleaned_song_url(href):
    return BASE_URL + href if "azlyrics" not in href else href

def get_song_list(list_album_items):
    return [item.text.lower() for item in list_album_items]

#sometimes the song doesn´t have a lyric meaning the anchor tag is empty
#so you have to catch the AttributeError on song_url(link)
def get_songs_links(response):
    soup = BeautifulSoup(response, 'html.parser')
    list_album_items = soup.find_all("div", class_="listalbum-item")
    songs_list = get_song_list(list_album_items)
    songs_dic = {}
    for link,song in zip(list_album_items,songs_list):
        try:
            songs_dic[song] = cleaned_song_url(song_url(link))
        except AttributeError:
            continue
    return songs_dic

#el try es por que aveces no hay href en una cancion
def fetch_song(artist_name, song_name, request=requests.get):
    #response = request(artist_url(artist_name))
    response = request(perform_search(artist_name))
    if response:
        songs_dic = get_songs_links(response.text)
        #return songs_dic.get(song_name.lower())
        return search_key_like(songs_dic,song_name.lower())
    return

def scraped_song_lyrics(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all("div")[24].text.replace('\r','')



def save(song_name):
    folder_name = 'json_lyrics'
    os.makedirs(folder_name,exist_ok=True)
    return open(f'{folder_name}/{song_name}.json','w')

            
def get_lyrics(artist_name='',song_name='',request=requests.get,
               save_json=False, return_json=False):
    if artist_name=='' or song_name=='':
        return "artist name and song name cannot be empty"
    song_url = fetch_song(artist_name,song_name,request)
    response = request(song_url)
    if response:
        lyrics = scraped_song_lyrics(response)
        data_json = {song_name:lyrics}
        json.dump(data_json, save(song_name)) if save_json else None 
        return lyrics if not return_json else data_json
    return



"""
usage:
artist_name -> a string with the name of the artist
song_name -> a string with the name of the song
request -> you can use your own request, default is requests.get
save_json -> when True a song_name.json is saved on the filesystem, default is False
return_text -> if you wish you can get the plain string ,default is False
"""




