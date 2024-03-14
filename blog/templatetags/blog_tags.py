from django import template
from django.db.models import Count

from blog.models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.published().count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.objects.published().order_by("-published_at")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return (
        Post.objects.published()
        .annotate(total_comments=Count("comments"))
        .order_by("-total_comments")[:count]
    )
