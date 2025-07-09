from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    """A topic abouy the user can write about."""

    text = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text


class Blog(models.Model):
    """A blog of a specific topic."""

    topic = models.ForeignKey(
        Topic, on_delete=models.SET_DEFAULT, default=1
    )
    title = models.CharField(max_length=60)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        """A string represeting the blog."""
        if len(self.title) > 50:
            return f"{self.title[:50]}..."
        else:
            return f"{self.title}"
