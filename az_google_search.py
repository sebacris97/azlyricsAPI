import httpx
import os

#GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
#SEARCH_ENGINE_ID = os.environ.get('SEARCH_ENGINE_ID')
GOOGLE_API_KEY="AIzaSyBkHSQ4sShpdS0CzpZAcyVZM9sm5OyfO6k"
SEARCH_ENGINE_ID="b68b26a7f065541a7"

def google_search(GOOGLE_API_KEY, SEARCH_ENGINE_ID, query, **params):
    params.update({
        'key': GOOGLE_API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        **params
    })
    base_url = 'https://www.googleapis.com/customsearch/v1'
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def perform_search(query):
    response = google_search(
            GOOGLE_API_KEY=GOOGLE_API_KEY,
            SEARCH_ENGINE_ID=SEARCH_ENGINE_ID,
            query=query,
            start=1
        )
    misstype = 'spelling' in response.keys()
    corrected_query = response['spelling']['correctedQuery'] if misstype else query
    link = response['items'][0]['link']
    return {'correct_name': corrected_query,
            'link': link}

