import pytest
from django.urls import reverse
from rest_framework import status

from .factories import UserFactory, LessonFactory, CourseFactory, CourseSubscriptionFactory


@pytest.fixture
def user_factory():
    yield UserFactory


@pytest.fixture
def course_factory():
    yield CourseFactory


@pytest.fixture
def lesson_factory():
    yield LessonFactory


@pytest.fixture
def course_subscription_factory():
    yield CourseSubscriptionFactory


@pytest.mark.django_db
def test_course_subscribe(api_client, course_factory, user_factory):
    course = course_factory()
    user = user_factory()
    api_client.force_authenticate(user=user)

    url = reverse("course-subscribe", kwargs={"pk": course.pk})
    response = api_client.post(url)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "Вы успешно подписались на курс."


@pytest.mark.django_db
def test_course_unsubscribe(api_client, course_factory, user_factory, course_subscription):
    course = course_factory()
    user = user_factory()
    subscription = course_subscription(course=course, user=user, is_active=True)
    api_client.force_authenticate(user=user)

    url = reverse("course-unsubscribe", kwargs={"pk": course.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT