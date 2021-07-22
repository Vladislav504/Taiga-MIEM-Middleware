import factory
import threading

from django.urls import reverse
from django.conf import settings


class Factory(factory.django.DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True

    _SEQUENCE = 1
    _SEQUENCE_LOCK = threading.Lock()

    @classmethod
    def _setup_next_sequence(cls):
        with cls._SEQUENCE_LOCK:
            cls._SEQUENCE += 1
        return cls._SEQUENCE


class ProjectTemplateFactory(Factory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = "projects.ProjectTemplate"
        django_get_or_create = ("slug", )

    name = "Template name"
    slug = settings.DEFAULT_PROJECT_TEMPLATE
    description = factory.Sequence(lambda n: "Description {}".format(n))

    us_statuses = []
    points = []
    task_statuses = []
    issue_statuses = []
    epic_statuses = []
    issue_types = []
    priorities = []
    severities = []
    roles = []
    us_custom_attributes = []
    task_custom_attributes = []
    issue_custom_attributes = []
    epic_custom_attributes = []
    default_owner_role = "tester"


class ProjectFactory(Factory):
    class Meta:
        model = "projects.Project"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Project {}".format(n))
    slug = factory.Sequence(lambda n: "project-{}-slug".format(n))
    description = "Project description"
    owner = factory.SubFactory("tests.factories.UserFactory")
    creation_template = factory.SubFactory(
        "tests.factories.ProjectTemplateFactory")


class UserFactory(Factory):
    class Meta:
        model = "users.User"
        strategy = factory.CREATE_STRATEGY

    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.LazyAttribute(lambda obj: '%s@email.com' % obj.username)
    password = factory.PostGeneration(
        lambda obj, *args, **kwargs: obj.set_password(obj.username))
    is_staff = False
    is_superuser = False


class RoleFactory(Factory):
    class Meta:
        model = "users.Role"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Role {}".format(n))
    slug = factory.Sequence(lambda n: "test-role-{}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class TrackingProjectFactory(Factory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = 'taiga_miem_middleware.TrackingProjects'

    project = factory.SubFactory("tests.factories.ProjectFactory")
    number = 0
    fullname = 'Test Project'


class UsersInviteFactory(Factory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = "taiga_miem_middleware.Leaderships"

    user = factory.SubFactory("tests.factories.UserFactory")
    role = factory.SubFactory("tests.factories.RoleFactory")
    project = factory.SubFactory("tests.factories.TrackingProjectFactory")
    email = factory.LazyAttribute(lambda obj: obj.user.email)
    is_leader = False
