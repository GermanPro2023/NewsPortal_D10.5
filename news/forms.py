from django import forms
from .models import Post, SubscribersCategory
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    content = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'author_name',
            'category_post',
            'header',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        header = cleaned_data.get("header")
        content = cleaned_data.get("content")

        if header == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = SubscribersCategory
        fields = ['category']