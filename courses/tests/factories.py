import factory
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from subscription.models import CourseSubscription
from ..models import User, Course, Lesson


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.LazyFunction(lambda: make_password('password'))
    city = factory.Faker('city')


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course

    name = factory.Sequence(lambda n: f'Course {n}')
    author = factory.SubFactory(UserFactory)


class LessonFactory(DjangoModelFactory):
    class Meta:
        model = Lesson

    name = factory.Sequence(lambda n: f'Lesson {n}')
    course = factory.SubFactory(CourseFactory)
    author = factory.SubFactory(UserFactory)


class CourseSubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = CourseSubscription

    course = factory.SubFactory(CourseFactory)
    user = factory.SubFactory(UserFactory)
    is_active = True
    active_since = factory.Faker('date')
