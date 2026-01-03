from django import forms
from .models import Idea, DevTool


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = [
            'title',
            'image',
            'content',
            'interest',
            'devtool',
            'interestAmount',
        ]
        
class DevtoolForm(forms.ModelForm):
    class Meta:
        model = DevTool
        fields = [
            'name',
            'type',
            'explain',
        ]
