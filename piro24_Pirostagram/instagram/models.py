# models.py
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    """
    기본 User를 그대로 쓰면서, 인스타처럼 '프로필(닉네임/소개/아바타)'만 확장하는 모델.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return f"Profile({self.user})"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="posts/%Y/%m/%d/")  # ✅ 1장

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["author", "-created_at"]),
        ]

    def __str__(self):
        return f"Post({self.id}) by {self.author}"

class Like(models.Model):
    """
    좋아요: (user, post) 유니크로 중복 좋아요 방지.
    토글은 view에서 있으면 삭제, 없으면 생성.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="uq_like_user_post")
        ]
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"Like(user={self.user_id}, post={self.post_id})"


class Comment(models.Model):
    """
    댓글: 작성/수정/삭제 구현용 최소 구성.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post", "created_at"]),
        ]

    def __str__(self):
        return f"Comment({self.id}) post={self.post_id} by {self.author}"


class Story(models.Model):
    """
    스토리 '묶음'(한 번 올리는 스토리 세트).
    여러 장 업로드는 StoryItem이 담당.
    24시간 만료 구현을 위해 expires_at을 둠.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["author", "-created_at"]),
            models.Index(fields=["-expires_at"]),
        ]

    def clean(self):
        if self.expires_at and self.expires_at <= timezone.now():
            raise ValidationError("expires_at must be in the future.")

    def __str__(self):
        return f"Story({self.id}) by {self.author}"

    @property
    def is_active(self) -> bool:
        return self.expires_at > timezone.now()


class StoryItem(models.Model):
    """
    스토리 안의 개별 이미지(여러 장).
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="items")
    image = models.ImageField(upload_to="stories/%Y/%m/%d/")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["story", "order"], name="uq_storyitem_story_order")
        ]

    def __str__(self):
        return f"StoryItem({self.id}) story={self.story_id} order={self.order}"


class Follow(models.Model):
    """
    팔로우 관계.
    follower(나) -> following(상대)
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_relations")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_relations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "following"], name="uq_follow_follower_following")
        ]
        indexes = [
            models.Index(fields=["follower"]),
            models.Index(fields=["following"]),
        ]

    def clean(self):
        # 자기 자신 팔로우 방지
        if self.follower_id and self.following_id and self.follower_id == self.following_id:
            raise ValidationError("You cannot follow yourself.")

    def save(self, *args, **kwargs):
        self.full_clean()  # clean() 호출되게
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Follow({self.follower_id} -> {self.following_id})"
