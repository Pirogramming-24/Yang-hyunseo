from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Post(models.Model) :
  movie_title = models.CharField(max_length=32) # 제목을 저장하는 필드 (최대 32자)
  release_year = models.CharField(max_length=32) # 제목을 저장하는 필드 (최대 32자)
  director_name = models.CharField(max_length=32)
  main_actor = models.CharField(max_length=32)
  genre = models.CharField(max_length=32) # 제목을 저장하는 필드 (최대 32자)
  rating = models.DecimalField(
    max_digits=2,      # 전체 자릿수
    decimal_places=1,  # 소수점 자릿수
    validators=[
        MinValueValidator(0.0),
        MaxValueValidator(5.0),
    ]
  )
  running_time = models.IntegerField()
  review_content = models.TextField() #긴 글
