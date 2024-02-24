import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_lesson_list(api_client, lesson_factory):
    lesson_factory.create_batch(5)

    url = reverse("lesson-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db
def test_lesson_create(api_client, course_factory, user_factory):
    course = course_factory()
    user = user_factory()
    api_client.force_authenticate(user=user)

    url = reverse("lesson-list")
    data = {
        "title": "Test Lesson",
        "content": "This is a test lesson",
        "course": course.pk,
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Test Lesson"


@pytest.mark.django_db
def test_lesson_retrieve(api_client, lesson_factory):
    lesson = lesson_factory()

    url = reverse("lesson-detail", kwargs={"pk": lesson.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == lesson.title


@pytest.mark.django_db
def test_lesson_update(api_client, lesson_factory, user_factory):
    lesson = lesson_factory()
    user = user_factory()
    api_client.force_authenticate(user=user)

    url = reverse("lesson-detail", kwargs={"pk": lesson.pk})
    data = {
        "title": "Updated Lesson",
        "content": "This is an updated lesson",
    }
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated Lesson"


@pytest.mark.django_db
def test_lesson_delete(api_client, lesson_factory, user_factory):
    lesson = lesson_factory()
    user = user_factory()
    api_client.force_authenticate(user=user)

    url = reverse("lesson-detail", kwargs={"pk": lesson.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
