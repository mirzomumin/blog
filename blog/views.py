# Create your views here.
from django.http import Http404
from django.shortcuts import render

from blog.models import Post


def post_list(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    context = {"posts": posts}
    return render(request, "blog/post/list.html", context)


def post_detail(request, id):
    try:
        post = Post.objects.get(id=id, status=Post.Status.PUBLISHED)
    except Post.DoesNotExist:
        raise Http404("No Post found.")

    context = {"post": post}
    return render(request, "blog/post/detail.html", context)
