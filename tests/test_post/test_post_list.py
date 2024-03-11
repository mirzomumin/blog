import pytest
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from tests.utils import create_post

User = get_user_model()


@pytest.mark.django_db
def test_post_list_empty_success(client):
    response = client.get("/blog/")
    ctx = response.context
    posts = ctx["posts"].object_list
    tag = ctx["tag"]

    assert response.status_code == 200
    assert len(posts) == 0
    assert tag is None


@pytest.mark.django_db
def test_post_list_success(client):
    user = User.objects.create_user(username="andy", password="andy_password")
    title = "My journey of becoming a software developer"
    text = "Then, we filter the list of posts by the ones that\
            contain the given tag. Since this is a many-to-ma-ny \
            relationship, we have to filter posts by \
            tags contained in a given list, which, in this case, \
            contains only one element. \
            We use the __in field lookup. Many-to-many relationships occur \
            when multiple objects of a model are associated \
            with multiple objects \
            of another model. In ourapplication, \
            a post can have multiple tags and \
            a tag can be related to multiple posts. You will."
    expected_post = create_post(
        title=title,
        body=text,
        user=user,
    )
    response = client.get("/blog/")
    ctx = response.context
    posts = ctx["posts"].object_list
    post = posts[0]
    tag = ctx["tag"]

    assert response.status_code == 200
    assert len(posts) == 1
    assert post.id == expected_post.id
    assert post.title == expected_post.title
    assert post.slug == expected_post.slug
    assert post.body == expected_post.body
    assert post.author == expected_post.author
    assert post.status == expected_post.status
    assert post.tags.first() == expected_post.tags.first()
    assert tag is None


@pytest.mark.parametrize(
    "page, post_length, post_index",
    [
        (1, 3, 3),
        (2, 1, 0),
    ],
)
@pytest.mark.django_db
def test_post_list_with_pagination_success(
    client,
    post_list: list,
    page: int,
    post_length: int,
    post_index: int,
):
    user = User.objects.create_user(username="azimjon", password="azimjon_password")
    for post in post_list:
        create_post(
            title=post["title"],
            body=post["text"],
            user=user,
            tags=post["tags"],
        )
    response = client.get(f"/blog/?page={page}")
    ctx = response.context
    posts = ctx["posts"].object_list
    post = posts[0]
    tag = ctx["tag"]

    assert response.status_code == 200
    assert len(posts) == post_length
    assert post.title == post_list[post_index]["title"]
    assert post.slug == slugify(post_list[post_index]["title"])
    assert post.body == post_list[post_index]["text"]
    assert post.author == user
    assert post.tags.first().name == post_list[post_index]["tags"][0]
    assert tag is None
