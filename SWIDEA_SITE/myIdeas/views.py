from django.shortcuts import render, redirect, get_object_or_404
from .models import DevTool, Idea, IdeaStar
from .forms import IdeaForm, DevtoolForm
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# @require_POST

def toggle_star(request, pk):
    idea = Idea.objects.get(id=pk)

    star_qs = IdeaStar.objects.filter(
        idea=idea
    )

    if star_qs.exists():
        # ⭐ 이미 찜한 상태 → 삭제
        star_qs.delete()
        starred = False
    else:
        # ⭐ 찜 안 한 상태 → 생성
        IdeaStar.objects.create(
            idea=idea
        )
        starred = True

    return JsonResponse({
        "starred": starred
    })

    
    
def update_interest(request, pk):
    idea = Idea.objects.get(id=pk)
    delta = int(request.POST.get("delta"))

    idea.interest += delta
    idea.interest = max(0, idea.interest)
    idea.save()

    return JsonResponse({
        "interest": idea.interest
    })

    
    
def ideas_list(request):
    sort = request.GET.get("sort", "latest")

    ideas = Idea.objects.all()

    if sort == "name":
        ideas = ideas.order_by("title")
    elif sort == "interest":
        ideas = ideas.order_by("-interest")
    elif sort == "star":
        ideas = ideas.order_by("-star_count")  # 아래에서 추가
    else:  # latest
        ideas = ideas.order_by("-id")

    return render(request, "ideas_list.html", {
        "ideas": ideas,
        "current_sort": sort,
    })


def ideas_read(request, pk):  
  idea = Idea.objects.get(id=pk) # DB에서 id가 pk인 게시글 하나 조회
  
  devtool = idea.devtool
  is_starred = IdeaStar.objects.filter(
        idea=idea
    ).exists()
  
  context = {
    "devtool" : devtool,
    "idea" : idea,
    "is_starred": is_starred,
  }
  return render(request, "ideas_read.html", context)

def ideas_create(request):
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect("myIdeas:ideas_read", pk=idea.pk) #pk를 전해줘야 하지 않나..?
    else:
        form = IdeaForm()

    return render(request, "ideas_create.html", {
        "form": form
    })
    

def ideas_update(request, pk):
    idea = get_object_or_404(Idea, id=pk)

    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect("myIdeas:ideas_read", pk=pk)
    else:
        form = IdeaForm(instance=idea)

    return render(request, "ideas_update.html", {
        "form": form,
        "idea": idea,
    })
    
def ideas_delete(request, pk):
    idea = get_object_or_404(Idea, id=pk)

    if request.method == "POST":
        idea.delete()
        return redirect("myIdeas:ideas_list")

    return render(request, "ideas_delete.html", {
        "idea": idea
    })


def devtool_list(request) :
    devtools = DevTool.objects.all() #DB에 저장된 모든 게시글 조회
    context = {
    "devtools" : devtools
    } #템플릿으로 전달할 데이터
    return render(request, "devtool_list.html", context) #context를 HTML 템플릿에 데이터를 넘김..?



def devtool_read(request, pk):
    devtool = DevTool.objects.get(id=pk)
    ideas = Idea.objects.filter(devtool=devtool)
    
    context = {
        "devtool": devtool,
        "ideas": ideas,
    }
    return render(request, "devtool_read.html", context) 


def devtool_create(request):
    if request.method == "POST":
        form = DevtoolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect("myIdeas:devtool_read", pk=devtool.pk)
    else:
        form = DevtoolForm()

    return render(request, "devtool_create.html", {"form": form})

def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, id=pk)

    if request.method == "POST":
        form = DevtoolForm(request.POST, request.FILES, instance=devtool)
        if form.is_valid():
            form.save()
            return redirect("myIdeas:devtool_read", pk=pk)
    else:
        form = DevtoolForm(instance=devtool)

    return render(request, "devtool_update.html", {
        "devtool": devtool,
        "form": form,
    })



def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, id=pk)

    if request.method == "POST":
        devtool.delete()
        return redirect("myIdeas:devtool_list")

    return render(request, "devtool_delete.html", {
        "devtool": devtool
    })
