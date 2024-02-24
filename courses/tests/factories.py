import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from subscription.models import CourseSubscription
from ..models import User, Course, Lesson


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
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


class CourseSubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = CourseSubscription

    user = factory.SubFactory(UserFactory)
    is_active = factory.Faker('boolean')
    active_since = factory.Faker('date_this_decade')

    @factory.lazy_attribute
    def course(self):
        return CourseFactory()


register(UserFactory)
register(CourseFactory)
register(LessonFactory)
register(CourseSubscriptionFactory)
