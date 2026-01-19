from django.shortcuts import render, HttpResponse, redirect
from .models import Post
from decimal import Decimal
from .forms import PostSearchForm
from django.db.models import Q

import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from langchain_upstage import ChatUpstage, UpstageEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate


# Create your views here.

# def hello_world(request) :
# 	return HttpResponse("Hello World")


from django.core.paginator import Paginator
from django.db.models import Q

def reviews_list(request):
    form = PostSearchForm(request.POST or None)
    posts = Post.objects.all()

    # 🔹 정렬 파라미터
    sort = request.GET.get("sort", "latest")

    if sort == "rating":
        posts = posts.order_by("-rating")
    elif sort == "title":
        posts = posts.order_by("movie_title")
    else:  # 최신 개봉순
        posts = posts.order_by("-release_year")

    # 🔹 검색
    if request.method == "POST" and form.is_valid():
        search_word = form.cleaned_data["search_word"]
        posts = posts.filter(
            Q(movie_title__icontains=search_word) |
            Q(director_name__icontains=search_word) |
            Q(main_actor__icontains=search_word)
        ).distinct()

    # 🔹 페이지네이션
    paginator = Paginator(posts, 6)  # 한 페이지 6개
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "reviews": page_obj,
        "page_obj": page_obj,
        "sort": sort,
    }
    return render(request, "reviews_list.html", context)




def reviews_read(request, pk):  
  review = Post.objects.get(id=pk) # DB에서 id가 pk인 게시글 하나 조회
  
  hours = review.running_time // 60
  minutes = review.running_time % 60
  context = {
    "review" : review,
    "hours" : hours,
    "minutes" : minutes,
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
  

def chat_bot(request):
  if request.method == "POST":
    return render(request, "reviews_chatbot.html")
  
  
  
def ping(request):
    return HttpResponse("ok")


# LLM 준비
llm = ChatUpstage(
    model="solar-mini",
    temperature=0.3   # 추천 설명은 약간 부드럽게
)


# 시스템 프롬프트
SYSTEM_PROMPT = """
너는 영화 추천 챗봇이다.
사용자의 요청에 맞게 주어진 영화 목록 안에서만 추천하라.
목록에 없는 영화는 절대 만들어내지 마라.
추천 이유를 한국어로 간결하게 설명하라.
"""


prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}\n\n영화 목록:\n{movies}")
])


@csrf_exempt
def ask(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    # 입력 파싱
    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        body = request.POST.dict()

    q = (body.get("question") or "").strip()
    if not q:
        return HttpResponseBadRequest("question required")

    # -----------------------------
    # 1️⃣ DB에서 영화 후보 찾기
    # -----------------------------
    # 질문을 키워드로 분리
    keywords = q.split()

    query = Q()
    for word in keywords:
        if len(word) < 2:
            continue
        query |= Q(movie_title__icontains=word)
        query |= Q(director_name__icontains=word)
        query |= Q(main_actor__icontains=word)
        query |= Q(genre__icontains=word)

    qs = Post.objects.filter(query).distinct()
    movies = qs[:10]

    # if not movies:
    #     return JsonResponse({
    #         "answer": " 조건에 맞는 영화를 찾지 못했어요 😢",
    #         "movies": []
    #     })
        
    if not movies:
      movies = Post.objects.order_by("-rating")[:5]


    # -----------------------------
    # 2️⃣ LLM에 넣을 컨텍스트 구성
    # -----------------------------
    movie_lines = []
    for m in movies:
        movie_lines.append(
            f"- {m.movie_title} ({m.release_year}) | "
            f"감독: {m.director_name}, 배우: {m.main_actor}, "
            f"장르: {m.genre}, 러닝타임: {m.running_time}분"
        )

    movie_context = "\n".join(movie_lines)

    # -----------------------------
    # 3️⃣ LLM 호출
    # -----------------------------
    messages = prompt.format_messages(
        question=q,
        movies=movie_context
    )

    answer = llm.invoke(messages).content

    # -----------------------------
    # 4️⃣ 응답
    # -----------------------------
    return JsonResponse({
        "answer": answer,
        "movies": [
            {
                "id": m.id,
                "title": m.movie_title,
                "poster": m.movie_poster.url if m.movie_poster else "",
                "rating": float(m.rating),
            }
            for m in movies
        ]
    })