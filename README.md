# azlyricsAPI

This project started as a FastAPI test — I'm still learning as I go.

The purpose of the API is to return the lyrics of a song from AZLyrics, given the artist's name and the song's title.

It is currently deployed on [aws](http://54.172.42.197:8000/api/get-lyrics/avril%20lavigne/what%20the%20hell/)
DEMO: [netlify](https://teal-bombolone-e98a8f.netlify.app/)

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

The `get_lyrics` function in `azlyricsbrave.py` supports:
- Passing a custom request function (e.g., from `requests`, `httpx`, or `requests_ip_rotator`), allowing flexibility in how requests are made.

---

## 🌐 External APIs Used

- **Brave Search API** – used to find the correct AZLyrics URL.

---

## 🚧 To-Do / Planned Improvements

- ~Add fuzzy matching support to the song name, similar to the artist name.~
  - ~⚠️ Note: Google Programmable Search allows only 100 searches per day on the free tier.~
- **Now i use brave api for searchs (2000 searchs p/month) and requests are reduced by one
    plus i get spellcheck on artist and song at the same time :D**
- Refactor and clean up the codebase (still in testing phase).
- Add support for multiple lyrics sources.
  - Users will be able to choose from which website they want to retrieve lyrics.
  - By default, AZLyrics will be used. If not found, fallback to other sites.


