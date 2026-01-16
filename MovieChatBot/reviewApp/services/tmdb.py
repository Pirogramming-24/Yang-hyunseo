# reviewApp/services/tmdb.py
import requests
from django.conf import settings

print("🔥 TMDB_API_KEY =", settings.TMDB_API_KEY)

BASE_URL = "https://api.themoviedb.org/3"


def fetch_movie_detail(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ko-KR"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()



def fetch_popular_movies(page=1):
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ko-KR",
        "page": page
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["results"]

def fetch_movie_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ko-KR"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def extract_director_and_actor(credits):
    director = None
    main_actor = None

    for crew in credits["crew"]:
        if crew["job"] == "Director":
            director = crew["name"]
            break

    if credits["cast"]:
        main_actor = credits["cast"][0]["name"]

    return director, main_actor
