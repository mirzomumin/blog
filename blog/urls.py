from django.urls import path

from blog.views import post_detail, post_list

app_name = "blog"

urlpatterns = [
    path("", post_list, name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/", post_detail, name="post_detail"
    ),
]
