import pytest
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse
from rest_framework import status

from .factories import CourseFactory, LessonFactory, UserFactory


@pytest.fixture
def api_client_with_user(api_client):
    user = UserFactory()
    access_token = AccessToken.for_user(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    api_client.force_authenticate(user=user)

    return api_client, user


@pytest.mark.django_db
def test_courses_list(api_client_with_user, django_assert_max_num_queries):
    api_client, user = api_client_with_user

    course1 = CourseFactory(author=user)
    course2 = CourseFactory(author=user)
    course3 = CourseFactory()

    with django_assert_max_num_queries(4):
        api_client.get(reverse("courses-list"), follow=True)

    response = api_client.get(reverse("courses-list"), follow=True)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 2


@pytest.mark.django_db
def test_course_retrieve(api_client_with_user):
    api_client, user = api_client_with_user
    course = CourseFactory(author=user)
    lessons = [LessonFactory(course=course) for _ in range(2)]

    response = api_client.get(
        reverse("courses-detail", args=[course.id]),
        follow=True
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == course.name
    assert len(response.json()["lessons"]) == 2


@pytest.mark.django_db
def test_lessons_list(api_client_with_user):
    api_client, user = api_client_with_user
    course = CourseFactory(author=user)
    lessons = [LessonFactory(course=course, author=user) for _ in range(4)]

    response = api_client.get(reverse("courses:lessons-list"), follow=True)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 4
    assert response.json()["count"] == 4


@pytest.mark.django_db
def test_course_subscribe(api_client_with_user):
    api_client, user = api_client_with_user
    course = CourseFactory(author=user)

    response = api_client.post(reverse("courses-subscribe", args=[course.id]))

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "Вы успешно подписались на курс."


@pytest.mark.django_db
def test_course_unsubscribe(api_client_with_user):
    api_client, user = api_client_with_user
    course = CourseFactory(author=user)

    # Subscribe to the course first
    api_client.post(reverse("courses-subscribe", args=[course.id]))

    response = api_client.delete(reverse("courses-unsubscribe", args=[course.id]))
    try_again_unsubscribe = api_client.delete(reverse("courses-unsubscribe", args=[course.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert try_again_unsubscribe.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_lesson_retrieve(api_client_with_user):
    api_client, user = api_client_with_user
    lesson = LessonFactory(author=user)

    response = api_client.get(reverse("courses:lessons-detail", args=[lesson.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == lesson.name
