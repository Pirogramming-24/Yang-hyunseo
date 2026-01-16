from django.core.management.base import BaseCommand
from reviewApp.models import Post
from reviewApp.services.tmdb import *

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w342"

class Command(BaseCommand):
    help = "Load movies from TMDB"

    def handle(self, *args, **kwargs):
        movies = fetch_popular_movies(page=1) + fetch_popular_movies(page=2)

        for movie in movies:
            if Post.objects.filter(movie_title=movie["title"]).exists():
                continue

            credits = fetch_movie_credits(movie["id"])
            director, actor = extract_director_and_actor(credits)

            detail = fetch_movie_detail(movie["id"])
            runtime = detail.get("runtime") or 0

            # 🎯 장르 처리
            genres = detail.get("genres", [])
            genre_names = [g["name"] for g in genres]
            genre_str = ", ".join(genre_names)

            poster_path = movie.get("poster_path")
            poster_url = (
                f"{IMAGE_BASE_URL}{poster_path}"
                if poster_path else ""
            )

            Post.objects.create(
                tmdb_id=movie["id"],
                movie_title=movie["title"],
                release_year=movie["release_date"][:4],
                movie_poster=poster_url,
                director_name=director or "Unknown",
                main_actor=actor or "Unknown",
                genre=genre_str,
                rating=round(movie["vote_average"] / 2, 1),
                running_time=runtime,
                review_content=movie["overview"]
            )

        self.stdout.write(self.style.SUCCESS("TMDB 영화 데이터 로딩 완료 🎬"))
