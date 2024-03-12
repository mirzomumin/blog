import pytest
from django.contrib.auth import get_user_model

from tests.utils import create_post

User = get_user_model()


@pytest.mark.django_db
def test_post_comment_success(client, post_list):
    user = User.objects.create_user(
        first_name="Andy",
        email="gmail@andy.com",
        username="andy",
        password="andy_password",
    )
    post_one = post_list[0]
    expected_post = create_post(
        user=user,
        title=post_one["title"],
        body=post_one["text"],
        tags=post_one["tags"],
    )
    url = (
        f"/blog/{expected_post.published_at.year}/"
        f"{expected_post.published_at.month}/"
        f"{expected_post.published_at.day}/"
        f"{expected_post.slug}/comment/"
    )
    data = {
        "name": user.first_name,
        "email": user.email,
        "body": "Nice post. I liked your thoughts.",
    }
    response = client.post(url, data=data)

    expected_comment = expected_post.comments.last()

    assert response.status_code == 200
    assert expected_comment.name == data["name"]
    assert expected_comment.email == data["email"]
    assert expected_comment.body == data["body"]


@pytest.mark.django_db
def test_post_comment_fail(client, post_list):
    user = User.objects.create_user(
        first_name="Andy",
        email="gmail@andy.com",
        username="andy",
        password="andy_password",
    )
    post_one = post_list[0]
    expected_post = create_post(
        user=user,
        title=post_one["title"],
        body=post_one["text"],
        tags=post_one["tags"],
    )
    url = (
        f"/blog/{expected_post.published_at.year}/"
        f"{expected_post.published_at.month}/"
        f"{expected_post.published_at.day}/"
        f"business/comment/"
    )
    data = {
        "name": user.first_name,
        "email": user.email,
        "body": "Nice post. I liked your thoughts.",
    }
    response = client.post(url, data=data)
    ctx = response.context

    assert response.status_code == 404
    assert ctx["exception"] == "No Post matches the given query."
