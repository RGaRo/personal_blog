from django import forms

from .models import Blog, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["text"]
        labels = {"text": ""}


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog

        fields = ["title", "text"]

        labels = {"title": "Title", "text": "Main content"}
