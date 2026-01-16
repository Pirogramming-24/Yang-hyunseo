from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Post(models.Model) :
  tmdb_id = models.IntegerField(unique=True)
  movie_poster = models.ImageField(
    upload_to="movie_img/",
    blank=True,
    null=True
)
  movie_title = models.CharField(max_length=32)
  release_year = models.CharField(max_length=32) 
  director_name = models.CharField(max_length=32)
  main_actor = models.CharField(max_length=32)
  genre = models.CharField(max_length=32) 
  rating = models.DecimalField(
    max_digits=2,      # 전체 자릿수
    decimal_places=1,  # 소수점 자릿수
    validators=[
        MinValueValidator(0.0),
        MaxValueValidator(5.0),
    ]
  )
  running_time = models.IntegerField()
  review_content = models.TextField() 
