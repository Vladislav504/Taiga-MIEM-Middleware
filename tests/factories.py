import uuid
import factory
import threading

from django.conf import settings

from .utils import DUMMY_BMP_DATA


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

    epic_statuses = []
    us_statuses = []
    us_duedates = []
    points = []
    task_statuses = []
    task_duedates = []
    issue_statuses = []
    issue_types = []
    issue_duedates = []
    priorities = []
    severities = []
    roles = []
    epic_custom_attributes = []
    us_custom_attributes = []
    task_custom_attributes = []
    issue_custom_attributes = []
    default_owner_role = "tester"


class ProjectFactory(Factory):
    class Meta:
        model = "projects.Project"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Project {}".format(n))
    slug = factory.Sequence(lambda n: "project-{}-slug".format(n))
    logo = factory.django.FileField(data=DUMMY_BMP_DATA)

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


class TaskStatusFactory(Factory):
    class Meta:
        model = "projects.TaskStatus"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Task status {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class IssueStatusFactory(Factory):
    class Meta:
        model = "projects.IssueStatus"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Issue Status {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class SeverityFactory(Factory):
    class Meta:
        model = "projects.Severity"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Severity {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class PriorityFactory(Factory):
    class Meta:
        model = "projects.Priority"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Priority {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class IssueTypeFactory(Factory):
    class Meta:
        model = "projects.IssueType"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Issue Type {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class UserStoryStatusFactory(Factory):
    class Meta:
        model = "projects.UserStoryStatus"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "User Story status {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class EpicStatusFactory(Factory):
    class Meta:
        model = "projects.EpicStatus"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Epic status {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class PointsFactory(Factory):
    class Meta:
        model = "projects.Points"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Points {}".format(n))
    value = 2
    project = factory.SubFactory("tests.factories.ProjectFactory")


class MembershipFactory(Factory):
    class Meta:
        model = "projects.Membership"
        strategy = factory.CREATE_STRATEGY

    token = factory.LazyAttribute(lambda obj: str(uuid.uuid1()))
    project = factory.SubFactory("tests.factories.ProjectFactory")
    role = factory.SubFactory("tests.factories.RoleFactory")
    user = factory.SubFactory("tests.factories.UserFactory")


def create_project(**kwargs):
    "Create a project along with its dependencies"
    defaults = {}
    defaults.update(kwargs)

    ProjectTemplateFactory.create(slug=settings.DEFAULT_PROJECT_TEMPLATE)

    project = ProjectFactory.create(**defaults)
    project.default_issue_status = IssueStatusFactory.create(project=project)
    project.default_severity = SeverityFactory.create(project=project)
    project.default_priority = PriorityFactory.create(project=project)
    project.default_issue_type = IssueTypeFactory.create(project=project)
    project.default_us_status = UserStoryStatusFactory.create(project=project)
    project.default_task_status = TaskStatusFactory.create(project=project)
    project.default_epic_status = EpicStatusFactory.create(project=project)
    project.default_points = PointsFactory.create(project=project)

    project.save()

    return project


class InvitationFactory(Factory):
    class Meta:
        model = "projects.Membership"
        strategy = factory.CREATE_STRATEGY

    token = factory.LazyAttribute(lambda obj: str(uuid.uuid1()))
    project = factory.SubFactory("tests.factories.ProjectFactory")
    role = factory.SubFactory("tests.factories.RoleFactory")
    email = factory.Sequence(lambda n: "user{}@email.com".format(n))


# !==================


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
