from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


def login_view(request):
    """
    커스텀 로그인
    """
    if request.user.is_authenticated:
        return redirect("instagram:main")

    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.GET.get("next", "instagram:main")
            return redirect(next_url)
        else:
            error = "아이디 또는 비밀번호가 올바르지 않습니다."

    return render(request, "login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("instagram:login")


def main_view(request):
    from .models import Post
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "main.html", {"posts": posts})

def user_search_view(request):
    from django.contrib.auth.models import User
    q = request.GET.get("q", "").strip()
    results = []
    
    if q:
        results = User.objects.filter(username__icontains=q).order_by('username')
    
    context = {"q": q, "results": results}
    return render(request, "user_search.html", context)

def make_post_view(request):
    return render(request, "make_post.html")

@login_required
def myprofile_view(request):
    from .models import Post
    user = request.user
    posts = user.posts.all().order_by('-created_at')
    context = {
        "user": user,
        "posts": posts
    }
    return render(request, "myprofile.html", context)


def othersprofile_view(request, user_id):
    from django.contrib.auth.models import User
    from .models import Post
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("instagram:main")
    
    posts = user.posts.all().order_by('-created_at')
    context = {
        "user": user,
        "posts": posts
    }
    return render(request, "othersprofile.html", context)

from .forms import PostCreateForm



@login_required
def make_post_view(request):
    """
    게시물 생성:
    - PostCreateForm으로 content와 image 받기
    """
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # 생성 후 홈(피드)로 이동
            return redirect("instagram:main")

    else:
        form = PostCreateForm()

    return render(request, "make_post.html", {"form": form})


@login_required
def follow_toggle_view(request, user_id):
    """
    팔로우/언팔로우 토글.
    POST 요청을 받아서 팔로우 상태를 토글함.
    """
    from django.contrib.auth.models import User
    from .models import Follow
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    
    if request.method != 'POST':
        return JsonResponse({"error": "POST method required"}, status=400)
    
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
    # 자신을 팔로우할 수 없음
    if target_user == request.user:
        return JsonResponse({"error": "Cannot follow yourself"}, status=400)
    
    # 팔로우 관계 확인
    follow_relation = Follow.objects.filter(
        follower=request.user,
        following=target_user
    ).first()
    
    if follow_relation:
        # 이미 팔로우 중이면 언팔로우
        follow_relation.delete()
        is_following = False
    else:
        # 팔로우하지 않았으면 팔로우
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )
        is_following = True
    
    return JsonResponse({
        "is_following": is_following,
        "followers_count": target_user.follower_relations.count(),
        "following_count": target_user.following_relations.count()
    })


@login_required
def like_toggle_view(request, post_id):
    """
    좋아요/좋아요 취소 토글.
    POST 요청을 받아서 좋아요 상태를 토글함.
    """
    from .models import Post, Like
    from django.http import JsonResponse
    
    if request.method != 'POST':
        return JsonResponse({"error": "POST method required"}, status=400)
    
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    
    # 좋아요 관계 확인
    like_relation = Like.objects.filter(
        user=request.user,
        post=post
    ).first()
    
    if like_relation:
        # 이미 좋아요 했으면 취소
        like_relation.delete()
        is_liked = False
    else:
        # 좋아요하지 않았으면 좋아요
        Like.objects.create(
            user=request.user,
            post=post
        )
        is_liked = True
    
    return JsonResponse({
        "is_liked": is_liked,
        "likes_count": post.likes.count()
    })

@login_required
def post_delete_view(request, post_id):
    """
    게시물 삭제: 본인의 게시물만 삭제 가능
    """
    from .models import Post
    from django.shortcuts import get_object_or_404
    
    post = get_object_or_404(Post, id=post_id)
    
    # 본인의 게시물이 아니면 403 Forbidden
    if post.author != request.user:
        return JsonResponse({"error": "Permission denied"}, status=403)
    
    post.delete()
    return JsonResponse({"success": True})


@login_required
def post_edit_view(request, post_id):
    """
    게시물 수정: content와 image 수정 가능
    """
    from .models import Post
    from django.shortcuts import get_object_or_404
    
    post = get_object_or_404(Post, id=post_id)
    
    # 본인의 게시물이 아니면 리다이렉트
    if post.author != request.user:
        return redirect("instagram:main")
    
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        post.content = content
        
        # 이미지 업로드 처리
        if "image" in request.FILES:
            post.image = request.FILES["image"]
        
        post.save()
        return redirect("instagram:myprofile")
    
    context = {"post": post}
    return render(request, "post_edit.html", context)


@login_required
def comment_create_view(request, post_id):
    """
    댓글 생성: AJAX로 처리
    """
    from .models import Post, Comment
    from django.shortcuts import get_object_or_404
    from django.http import JsonResponse
    
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)
    
    post = get_object_or_404(Post, id=post_id)
    
    content = request.POST.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "Content is required"}, status=400)
    
    comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=content
    )
    
    return JsonResponse({
        "success": True,
        "comment": {
            "id": comment.id,
            "author": comment.author.username,
            "content": comment.content,
            "created_at": comment.created_at.strftime("%Y년 %m월 %d일 %H:%M")
        }
    })


@login_required
def comment_delete_view(request, comment_id):
    """
    댓글 삭제: 본인의 댓글만 삭제 가능
    """
    from .models import Comment
    from django.shortcuts import get_object_or_404
    
    comment = get_object_or_404(Comment, id=comment_id)
    
    # 본인의 댓글이 아니면 403 Forbidden
    if comment.author != request.user:
        return JsonResponse({"error": "Permission denied"}, status=403)
    
    comment.delete()
    return JsonResponse({"success": True})


@login_required
def story_create_view(request):
    """
    스토리 업로드: 이미지 받아서 Story + StoryItem 생성
    """
    from .models import Story, StoryItem
    from django.utils import timezone
    from datetime import timedelta
    from django.http import JsonResponse
    
    if request.method == "POST" and request.FILES.get("image"):
        # 24시간 후 만료 설정
        expires_at = timezone.now() + timedelta(hours=24)
        
        # Story 생성
        story = Story.objects.create(
            author=request.user,
            expires_at=expires_at
        )
        
        # StoryItem 생성 (이미지)
        image = request.FILES.get("image")
        StoryItem.objects.create(
            story=story,
            image=image,
            order=1
        )
        
        return JsonResponse({"success": True, "story_id": story.id})
    
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def story_list_view(request):
    """
    스토리 목록: 활성화된 스토리가 있는 사용자 목록 반환
    """
    from .models import Story
    from django.utils import timezone
    
    # 만료되지 않은 활성 스토리 조회
    active_stories = Story.objects.filter(
        expires_at__gt=timezone.now()
    ).select_related('author').order_by('-created_at')
    
    # 사용자별로 가장 최신 스토리만 추출 (Python에서 처리)
    users_with_stories = {}
    for story in active_stories:
        if story.author_id not in users_with_stories:
            avatar_url = None
            try:
                if story.author.profile and story.author.profile.avatar:
                    avatar_url = story.author.profile.avatar.url
            except:
                pass
            
            users_with_stories[story.author_id] = {
                'user_id': story.author.id,
                'username': story.author.username,
                'avatar': avatar_url,
                'story_id': story.id
            }
    
    # 현재 사용자를 맨 앞에 배치
    result = []
    current_user_story = None
    
    for user_id, user_data in users_with_stories.items():
        if user_id == request.user.id:
            current_user_story = user_data
        else:
            result.append(user_data)
    
    if current_user_story:
        result.insert(0, current_user_story)
    
    return JsonResponse({"users": result})


@login_required
def story_detail_view(request, user_id):
    """
    특정 사용자의 스토리 보기
    """
    from .models import Story
    from django.shortcuts import get_object_or_404
    from django.contrib.auth.models import User as DjangoUser
    from django.utils import timezone
    
    target_user = get_object_or_404(DjangoUser, id=user_id)
    
    # 해당 사용자의 활성 스토리 조회
    stories = Story.objects.filter(
        author=target_user,
        expires_at__gt=timezone.now()
    ).order_by('-created_at')
    
    context = {
        'target_user': target_user,
        'stories': stories
    }
    
    return render(request, 'story_detail.html', context)
