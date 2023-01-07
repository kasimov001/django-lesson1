from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe, Tag, RecipeIngredient


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["author", 'title', 'is_active', 'tags']
        exclude = ['slug', "author"]

        def clean_title(self):
            title = self.cleaned_data['title']
            print(self.cleaned_data)
            if len(title) < 5:
                raise ValidationError("title 10 ta belgidan koproq bolishi kerak")
            if title.capitalize() != title:
                raise ValidationError("Bosh Xarf Bilan Yozilish Kerak ")
            return title

        # def clean(self):
        #     title = self.cleaned_data['title']
        #     if len(title) < 10:
        #         raise ValidationError("title 10 ta belgidan koproq bolishi kerak")
        #     return title

    def __init__(self, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Recipe...'
        })
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control tags',
        })


class RecipeUpdateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['id', "auther", 'title', 'is_active', 'tags']
        exclude = ["auther"]

    def __init__(self, *args, **kwargs):
        super(RecipeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Recipe...'
        })
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control tags',
        })
        self.fields['is_active'].widget.attrs.update({
            'class': 'form-control',
        })


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tag...'
        })


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'
        exclude = ['recipe']

    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingredient...'
        })
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['unit'].widget.attrs.update({
            'class': 'form-control',
        })
