import pytest
from django.contrib.auth import get_user_model

from tests.utils import create_comment, create_post

User = get_user_model()


@pytest.mark.django_db
def test_post_detail_success(client):
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
    url = (
        f"/blog/{expected_post.published_at.year}/"
        f"{expected_post.published_at.month}/"
        f"{expected_post.published_at.day}/"
        f"{expected_post.slug}/"
    )
    response = client.get(url)
    ctx = response.context
    post = ctx["post"]
    comments = ctx["comments"]

    # check post
    assert response.status_code == 200
    assert post.id == expected_post.id
    assert post.title == expected_post.title
    assert post.slug == expected_post.slug
    assert post.body == expected_post.body
    assert post.author == expected_post.author
    assert post.status == expected_post.status
    assert post.tags.first() == expected_post.tags.first()

    # check comments
    assert len(comments) == 0


@pytest.mark.django_db
def test_post_detail_with_comments_success(client):
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
    expected_comment = create_comment(
        post_id=expected_post.id,
        name="User",
        email="user@gmail.com",
        body=(
            "You will learn how to build complex "
            "QuerySets to retrieve objects by similarity."
        ),
    )
    url = (
        f"/blog/{expected_post.published_at.year}/"
        f"{expected_post.published_at.month}/"
        f"{expected_post.published_at.day}/"
        f"{expected_post.slug}/"
    )
    response = client.get(url)
    ctx = response.context
    post = ctx["post"]
    comments = ctx["comments"]
    comment = comments[0]

    # check post
    assert response.status_code == 200
    assert post.id == expected_post.id
    assert post.title == expected_post.title
    assert post.slug == expected_post.slug
    assert post.body == expected_post.body
    assert post.author == expected_post.author
    assert post.status == expected_post.status
    assert post.tags.first() == expected_post.tags.first()

    # check comments
    assert len(comments) == 1
    assert comment.post_id == expected_comment.post_id
    assert comment.name == expected_comment.name
    assert comment.email == expected_comment.email
    assert comment.body == expected_comment.body


@pytest.mark.django_db
def test_post_detail_fail(client):
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
    url = (
        f"/blog/{expected_post.published_at.year}/"
        f"{expected_post.published_at.month}/"
        f"{expected_post.published_at.day}/"
        f"{expected_post.slug}-user/"
    )
    response = client.get(url)
    ctx = response.context

    assert response.status_code == 404
    assert ctx["exception"] == "No Post found."
