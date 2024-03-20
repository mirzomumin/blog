from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404
from taggit.models import Tag

from blog.forms import CommentForm, EmailPostForm, SearchForm
from blog.models import Post


def post_search_service(request: HttpRequest) -> dict:
    form = SearchForm()
    query = None
    results = []

    if "query" not in request.GET:
        context = {"form": form, "query": query, "results": results}
        return context

    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data["query"]
        results = (
            Post.objects.published()
            .annotate(similarity=TrigramSimilarity("title", query))
            .filter(similarity__gt=0.1)
            .order_by("-similarity")
        )

    context = {"form": form, "query": query, "results": results}
    return context


def post_list_service(request: HttpRequest, tag_slug: str) -> dict:
    post_list = Post.objects.published()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {"posts": posts, "tag": tag}
    return context


def post_detail_service(
    request: HttpRequest,
    year: int,
    month: int,
    day: int,
    post: str,
) -> dict:
    try:
        post = Post.objects.get(
            status=Post.Status.PUBLISHED,
            slug=post,
            published_at__year=year,
            published_at__month=month,
            published_at__day=day,
        )
    except Post.DoesNotExist:
        raise Http404("No Post found.")

    comments = post.comments.filter(is_active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = (
        Post.objects.published(tags__in=post_tags_ids)
        .exclude(id=post.id)
        .annotate(same_tags=Count("tags"))
        .order_by(
            "-same_tags",
            "-published_at",
        )
    )

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "similar_posts": similar_posts,
    }
    return context


def post_share_service(
    request: HttpRequest,
    year: int,
    month: int,
    day: int,
    post: str,
) -> dict:
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        published_at__year=year,
        published_at__month=month,
        published_at__day=day,
    )
    is_sent = False

    if request.method != "POST":
        form = EmailPostForm()
        context = {"post": post, "form": form, "is_sent": is_sent}
        return context

    form = EmailPostForm(request.POST)
    if not form.is_valid():
        context = {"post": post, "form": form, "is_sent": is_sent}
        return context

    cleaned_data = form.cleaned_data
    post_url = request.build_absolute_uri(post.get_absolute_url())
    subject = f'{cleaned_data["name"]} recommends you read {post.title}'
    message = (
        f'Read {post.title} at {post_url}\n\n'
        f'{cleaned_data["name"]}\'s comments: {cleaned_data["comments"]}'
    )
    response = send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [cleaned_data["to"]],
        fail_silently=False,
    )
    is_sent = bool(response)

    context = {"post": post, "form": form, "is_sent": is_sent}
    return context


def post_comment_service(
    request: HttpRequest,
    year: int,
    month: int,
    day: int,
    post: str,
) -> dict:
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        published_at__year=year,
        published_at__month=month,
        published_at__day=day,
    )
    comment = None

    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()

    context = {"post": post, "form": form, "comment": comment}
    return context
