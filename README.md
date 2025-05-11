# azlyricsAPI

This project started as a FastAPI test — I'm still learning as I go.

The purpose of the API is to return the lyrics of a song from AZLyrics, given the artist's name and the song's title.

It is currently deployed on [aws](http://54.172.42.197:8000/api/get-lyrics/avril%20lavigne/what%20the%20hell/)

---

## 🔧 How It Works

To use the API, pass the artist name and the song name in the URL like this:

```
entry-point.com/get-lyrics/olivia rodrigo/brutal
```

If successful, it returns the lyrics scraped from AZLyrics in this format:

```json
{
  "artist": "olivia rodrigo",
  "song": "brutal",
  "lyrics": "lorem ipsum..."
}
```

---

## ⚙️ Functionality

The `get_lyrics` function in `azlyrics_scraper.py` supports:

- Returning just the lyrics as a plain text.
- Passing a custom request function (e.g., from `requests`, `httpx`, or `requests_ip_rotator`), allowing flexibility in how requests are made.

---

## 🌐 External APIs Used

- **Google Custom Search API** – used to find the correct AZLyrics URL.

---

## 🚧 To-Do / Planned Improvements

- Add fuzzy matching support to the song name, similar to the artist name.
  - ⚠️ Note: Google Programmable Search allows only 100 searches per day on the free tier.
- Refactor and clean up the codebase (still in testing phase).
- Add support for multiple lyrics sources.
  - Users will be able to choose from which website they want to retrieve lyrics.
  - By default, AZLyrics will be used. If not found, fallback to other sites.


