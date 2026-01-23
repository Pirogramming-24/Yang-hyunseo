import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from .models import Conversation, Message
from .services.huggingface import run_ai as hf_run_ai

import traceback

from .models import Conversation, Message


def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "signup.html", {
                "error": "비밀번호가 일치하지 않습니다."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "이미 존재하는 아이디입니다."
            })

        user = User.objects.create_user(
            username=username,
            password=password1,
            first_name=name
        )
        user.save()

        return redirect("login")

    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("main")  # 로그인 후 이동할 페이지
        else:
            return render(request, "login.html", {
                "error": "아이디 또는 비밀번호가 올바르지 않습니다."
            })

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def main_view(request):
    return render(request, "main.html")

@login_required
def generate_view(request):
    messages = []

    if request.user.is_authenticated:
        messages = Message.objects.filter(
            conversation__user=request.user,
            conversation__model_type="generate"
        ).order_by("created_at")

    return render(request, "generate.html", {
        "messages": messages
    })
    
def translate_view(request):
    messages = []

    if request.user.is_authenticated:
        messages = Message.objects.filter(
            conversation__user=request.user,
            conversation__model_type="translate"
        ).order_by("created_at")

    return render(request, "translate.html", {
        "messages": messages
    })
    
def sentiment_view(request):
    messages = []

    if request.user.is_authenticated:
        messages = Message.objects.filter(
            conversation__user=request.user,
            conversation__model_type="sentiment"
        ).order_by("created_at")

    return render(request, "sentiment.html", {
        "messages": messages
    })

@csrf_exempt
@require_POST
def run_ai_view(request, model_type):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "invalid json"}, status=400)

    user_input = (body.get("message") or "").strip()
    if not user_input:
        return JsonResponse({"error": "empty message"}, status=400)

    conversation = None
    if request.user.is_authenticated:
        conversation = Conversation.objects.create(
            user=request.user,
            model_type=model_type,
        )
        Message.objects.create(
            conversation=conversation,
            role="user",
            content=user_input
        )

    try:
        assistant_reply = hf_run_ai(model_type, user_input)

    except Exception as e:
        print("🔥 GENERATE ERROR 🔥")
        traceback.print_exc()   # ← 이 줄 핵심
        return JsonResponse({"error": str(e)}, status=502)

    if conversation:
        Message.objects.create(
            conversation=conversation,
            role="assistant",
            content=assistant_reply
        )

    return JsonResponse({"reply": assistant_reply})





