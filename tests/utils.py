from django.contrib.auth import get_user_model
from django.utils.text import slugify

from blog.models import Comment, Post

User = get_user_model()


def create_post(
    title: str,
    body: str,
    user: User,  # type: ignore
    status: str = Post.Status.PUBLISHED,
    tags: list[str] = ["IT"],
) -> Post:  # type: ignore
    slug = slugify(title)
    post = Post.objects.create(
        title=title,
        slug=slug,
        author=user,
        body=body,
        status=status,
    )
    post.tags.add(*tags)
    return post


def create_comment(
    post_id: int,
    name: str,
    email: str,
    body: str,
):
    comment = Comment.objects.create(
        post_id=post_id,
        name=name,
        email=email,
        body=body,
    )

    return comment
