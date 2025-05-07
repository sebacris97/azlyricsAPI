from azlyrics_scraper import get_lyrics
import requests


def extern_request(url):
    TOKEN = "MY_SECRET_TOKEN"
    SCRAP_URL = "https://my-scraper-api-url.com/"
    PAYLOAD = { 'api_key': TOKEN, 'url': url,
                'follow_redirect': 'true', 'retry_404': 'true' }
    return requests.get(SCRAP_URL, params=PAYLOAD)


"""
for avoid ip blocking from azlyrics servers
you can use your own request, this gives you the possibility
to use any Web Scraping API you wish as long as the return value
is a response from requests.get
default request is requests.get
"""

#recommended for high volume requests
#lyrics = get_lyrics('olivia rodrigo','brutal',request=extern_request)

lyrics = get_lyrics(
                    artist_name = 'olivia rodrigo',
                    song_name = 'brutal',
                    #request = extern_request,
                    save_json = True,
                    return_json = True
                    )
print(lyrics)

