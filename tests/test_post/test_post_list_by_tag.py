import pytest
from django.contrib.auth import get_user_model

from tests.utils import create_post

User = get_user_model()


@pytest.mark.django_db
def test_post_list_by_tag_success(client):
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
    expected_tag = expected_post.tags.first()
    response = client.get(f"/blog/tag/{expected_tag.slug}/")
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
    assert tag == expected_tag


@pytest.mark.django_db
def test_post_list_by_tag_fail(client):
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
    create_post(
        title=title,
        body=text,
        user=user,
    )
    response = client.get("/blog/tag/business/")
    ctx = response.context
    expected_exception = "No Tag matches the given query."

    assert response.status_code == 404
    assert ctx["exception"] == expected_exception
