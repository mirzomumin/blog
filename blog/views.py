# Create your views here.
from django.http import Http404
from django.shortcuts import render

from blog.models import Post


def post_list(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    context = {"posts": posts}
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

    context = {"post": post}
    return render(request, "blog/post/detail.html", context)
