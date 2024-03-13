# Create your views here.
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from taggit.models import Tag

from blog.forms import CommentForm, EmailPostForm
from blog.models import Post


def post_list(request, tag_slug=None):
    post_list = Post.objects.filter(status=Post.Status.PUBLISHED)
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
    return render(request, "blog/post/list.html", context)


def post_detail(request, year, month, day, post):
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
        Post.objects.filter(status=Post.Status.PUBLISHED, tags__in=post_tags_ids)
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
    return render(request, "blog/post/detail.html", context)


def post_share(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        published_at__year=year,
        published_at__month=month,
        published_at__day=day,
    )
    is_sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
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

    else:
        form = EmailPostForm()

    context = {"post": post, "form": form, "is_sent": is_sent}
    return render(request, "blog/post/share.html", context)


@require_POST
def post_comment(request, year, month, day, post):
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
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )
