from django import forms
from .models import Article


class Articleform(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'content']