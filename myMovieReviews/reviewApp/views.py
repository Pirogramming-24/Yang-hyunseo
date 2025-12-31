from django.shortcuts import render, HttpResponse, redirect
from .models import Post 
from decimal import Decimal


# Create your views here.

# def hello_world(request) :
# 	return HttpResponse("Hello World")


def reviews_list(request) :
  reviews = Post.objects.all() #DB에 저장된 모든 게시글 조회
  context = {
    "reviews" : reviews
  } #템플릿으로 전달할 데이터
  return render(request, "reviews_list.html", context) #context를 HTML 템플릿에 데이터를 넘김..?


def reviews_read(request, pk):  
  review = Post.objects.get(id=pk) # DB에서 id가 pk인 게시글 하나 조회
  context = {
    "review" : review
  }
  return render(request, "reviews_read.html", context)



def reviews_create(request):
    if request.method == "POST":
        Post.objects.create(
            movie_title=request.POST["movie_title"],
            release_year=request.POST["release_year"],
            director_name=request.POST["director_name"],
            main_actor=request.POST["main_actor"],
            genre=request.POST["genre"],
            rating=request.POST["rating"],
            running_time=request.POST["running_time"],
            review_content=request.POST["review_content"],
        )
        return redirect("reviewApp:reviews_list")

    return render(request, "reviews_create.html")


def reviews_update(request, pk):
    review = Post.objects.get(id=pk) #URL에서 받은 pk로 DB에서 게시글 조회

    if request.method == "POST":
        review.movie_title=request.POST["movie_title"]
        review.release_year=request.POST["release_year"]
        review.director_name=request.POST["director_name"]
        review.main_actor=request.POST["main_actor"]
        review.genre=request.POST["genre"]
        review.rating = Decimal(request.POST["rating"])
        review.rating = Decimal(request.POST["rating"])
        review.review_content=request.POST["review_content"]
        review.save()
        #return redirect(f"/posts/{pk}/")
        return redirect("reviewApp:read", pk=pk) # 수정 후 상세 페이지로 리다이렉트

    context = {"review": review}
    return render(request, "reviews_update.html", context)


def reviews_delete(request, pk):
    if request.method == "POST":
        review = Post.objects.get(id=pk) #pk로 삭제 대상 게시글을 DB에서 조회
        review.delete() #해당 게시글을 DB에서 완전히 삭제
    return redirect("reviewApp:reviews_list") #삭제 후 게시글 목록 페이지로 리다이렉트
