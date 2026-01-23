# forms.py  (게시물 업로드용)
from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "placeholder": "문구를 입력하세요..."})
        }


class PostUpdateForm(forms.ModelForm):
    """
    게시물 수정 폼:
    - 보통 content만 수정 가능하게(인스타처럼)
    - 이미지 수정까지 하려면 별도 UI/로직이 필요해서 여기선 분리
    """
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "문구를 수정하세요...",
            })
        }
