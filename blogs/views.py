from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from .models import Topic, Blog
from .forms import TopicForm, BlogForm
from django.utils import timezone
from django.db.models import Q

# Create your views here.


def home_page(request):
    """The home page for out blog."""
    return render(request, "blogs/home_page.html")


@login_required
def topics(request):
    topics = (
        Topic.objects.all()
        .filter(owner=request.user)
        .order_by("-date_added")
    )
    content = {"topics": topics}
    return render(request, "blogs/topics.html", content)


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_ownership_topic(topic.owner, request.user)
    blogs = Blog.objects.filter(
        topic_id=topic_id, deleted=False
    ).order_by("-date_added")
    content = {"topic": topic, "blogs": blogs}
    return render(request, "blogs/topic.html", content)


@login_required
def blog(request, topic_id, blog_id):
    topic = Topic.objects.get(id=topic_id)
    check_ownership_topic(topic.owner, request.user)
    blog = Blog.objects.filter(
        topic_id=topic_id, id=blog_id, deleted=False
    )
    content = {"topic": topic, "blog": blog}
    return render(request, "blogs/blog.html", content)


def public_blog(request, blog_id):
    blog = Blog.objects.filter(id=blog_id, deleted=False)
    content = {"blog": blog}
    return render(request, "blogs/public_blog.html", content)


@login_required
def new_topic(request):
    """Add a new topic."""
    user = User.objects.get(id=request.user.id)
    if request.method != "POST":
        # No data submitted; create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = user
            new_topic.save()
            return redirect("blogs:topics")

    context = {"form": form}
    return render(request, "blogs/new_topic.html", context)


@login_required
def new_blog(request, topic_id):
    """Add a new blog."""
    topic = Topic.objects.get(id=topic_id)
    user = User.objects.get(id=request.user.id)
    check_ownership_topic(topic.owner, request.user)

    if request.method != "POST":
        # No data submitted; create a blank form
        form = BlogForm()
    else:
        # POST data submitted; process data
        form = BlogForm(data=request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = user
            blog.topic = topic
            form.save()
            return redirect("blogs:topic", topic_id=topic_id)

    context = {"form": form, "topic": topic}
    return render(request, "blogs/new_blog.html", context)


@login_required
def edit_topic(request, topic_id):
    """Edit an existing topic."""
    topic = Topic.objects.get(id=topic_id)
    check_ownership_topic(topic.owner, request.user)

    if request.method != "POST":
        # Initial request
        form = TopicForm(instance=topic)
    else:
        # POST data submitted
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("blogs:topics")
    context = {"form": form, "topic": topic}
    return render(request, "blogs/edit_topic.html", context)


@login_required
def edit_blog(request, topic_id, blog_id):
    """Edit an existing topic."""
    topic = Topic.objects.get(id=topic_id)
    blog = Blog.objects.get(id=blog_id)
    check_ownership_topic(topic.owner, request.user)
    check_blog_topic(blog.topic, topic)

    if request.method != "POST":
        # Initial request
        form = BlogForm(instance=blog)
    else:
        # POST data submitted
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            updated_blog = form.save(
                commit=False
            )  # aún no guarda en BD
            updated_blog.date_last_modified = timezone.now()
            updated_blog.save()
            return redirect(
                "blogs:blog_detail", topic_id=topic_id, blog_id=blog_id
            )
    context = {"form": form, "topic": topic, "blog": blog}
    return render(request, "blogs/edit_blog.html", context)


@login_required
def delete_blog(request, topic_id, blog_id):
    """Edit an existing topic."""
    topic = Topic.objects.get(id=topic_id)
    blog = Blog.objects.get(id=blog_id)
    check_ownership_topic(topic.owner, request.user)
    check_blog_topic(blog.topic, topic)

    if request.method == "POST":
        blog.deleted = True  # 👈 Soft delete
        blog.save()
        return redirect("blogs:topic", topic_id=topic.id)

    context = {"blog": blog, "topic": topic}
    return render(request, "blogs/delete_blog.html", context)


def search(request):
    """
    Finder bar view.

    • If no query, show ALL blogs ordered by newest.
    • Otherwise filter by title OR body text (case-insensitive).
    """
    query = request.GET.get("q", "").strip().lower()

    # Start with all blogs sorted newest-first
    blogs = (
        Blog.objects.select_related("topic")
        .order_by("-date_added")
        .filter(deleted=False)
    )

    # Apply filter only when query provided
    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) | Q(text__icontains=query),
            deleted=False,
        )

    return render(
        request, "blogs/search.html", {"query": query, "blogs": blogs}
    )


def check_ownership_topic(topic_owner, request_user):
    if topic_owner != request_user:
        raise Http404


def check_blog_topic(blog_topic, topic):
    if blog_topic != topic:
        raise Http404
