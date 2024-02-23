# Create your views here.
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render

from blog.models import Post


def post_list(request):
    post_list = Post.objects.filter(status=Post.Status.PUBLISHED)

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
