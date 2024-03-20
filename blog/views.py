# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_POST

from blog import services


def post_search(request):
    context = services.post_search_service(request)
    return render(request, "blog/post/search.html", context)


def post_list(request, tag_slug=None):
    context = services.post_list_service(request, tag_slug)
    return render(request, "blog/post/list.html", context)


def post_detail(request, year, month, day, post):
    context = services.post_detail_service(request, year, month, day, post)
    return render(request, "blog/post/detail.html", context)


def post_share(request, year, month, day, post):
    context = services.post_share_service(request, year, month, day, post)
    return render(request, "blog/post/share.html", context)


@require_POST
def post_comment(request, year, month, day, post):
    context = services.post_comment_service(request, year, month, day, post)
    return render(request, "blog/post/comment.html", context)
