"""Define urls patterns for blog app."""

from django.urls import path

from . import views

app_name = "blogs"
urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("topics/", views.topics, name="topics"),
    path("topic/<int:topic_id>/", views.topic, name="topic"),
    path(
        "blogs/<int:topic_id>/<int:blog_id>/",
        views.blog,
        name="blog_detail",
    ),
    path("new_topic/", views.new_topic, name="new_topic"),
    path("new_blog/<int:topic_id>", views.new_blog, name="new_blog"),
    path("edit_topic/<int:topic_id>", views.edit_topic, name="edit_topic"),
    path(
        "edit_blog/<int:topic_id>/<int:blog_id>/",
        views.edit_blog,
        name="edit_blog",
    ),
    path("search/", views.search, name="search"),
    path(
        "public_blog/<int:blog_id>",
        views.public_blog,
        name="public_blog",
    ),
    path(
        "edit_blog/<int:topic_id>/<int:blog_id>/delete/",
        views.delete_blog,
        name="delete_blog",
    ),
]
