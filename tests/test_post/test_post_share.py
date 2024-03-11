import pytest
from django.contrib.auth import get_user_model

from tests.utils import create_post

User = get_user_model()


@pytest.mark.django_db
def test_post_share_success(client, post_list, mocker):
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
        f"{expected_post.slug}/share/"
    )
    data = {
        "name": user.first_name,
        "email": user.email,
        "to": "some@mail.ru",
        "comments": "Absolutely amazing post!",
    }
    mocker.patch("django.core.mail.send_mail", return_value=1)
    response = client.post(url, data=data)

    ctx = response.context

    assert response.status_code == 200
    assert ctx["is_sent"] is True


@pytest.mark.django_db
def test_post_share_fail(client, post_list, mocker):
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
        f"business/share/"
    )
    data = {
        "name": user.first_name,
        "email": user.email,
        "to": "some@mail.ru",
        "comments": "Absolutely amazing post!",
    }
    mocker.patch("django.core.mail.send_mail", return_value=1)
    response = client.post(url, data=data)
    ctx = response.context

    assert response.status_code == 404
    assert ctx["exception"] == "No Post matches the given query."
