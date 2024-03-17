from django.urls import path

from blog.feeds import LatestPostsFeed
from blog.views import (post_comment, post_detail, post_list, post_search,
                        post_share)

app_name = "blog"

urlpatterns = [
    path("", post_list, name="post_list"),
    path("tag/<slug:tag_slug>/", post_list, name="post_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        post_detail,
        name="post_detail",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/share/",
        post_share,
        name="post_share",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/comment/",
        post_comment,
        name="post_comment",
    ),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("search/", post_search, name="post_search"),
]
