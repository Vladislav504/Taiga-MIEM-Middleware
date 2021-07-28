import pytest
from unittest import mock
import functools

from . import factories as f


class PartialMethodCaller:
    def __init__(self, obj, **partial_params):
        self.obj = obj
        self.partial_params = partial_params

    def __getattr__(self, name):
        return functools.partial(getattr(self.obj, name),
                                 **self.partial_params)


@pytest.fixture
def client():
    from django.test.client import Client

    class _Client(Client):
        def login(self,
                  user=None,
                  backend="django.contrib.auth.backends.ModelBackend",
                  **credentials):
            if user is None:
                return super().login(**credentials)

            with mock.patch(
                    'django.contrib.auth.authenticate') as authenticate:
                user.backend = backend
                authenticate.return_value = user
                return super().login(**credentials)

        @property
        def json(self):
            return PartialMethodCaller(
                obj=self, content_type='application/json;charset="utf-8"')

    return _Client()


@pytest.fixture
def admin_client(client):
    admin = f.UserFactory(is_superuser=True)
    client.login(admin)
    return client


@pytest.fixture
def just_user():
    just_user = f.UserFactory()
    just_user.save()
    return just_user


@pytest.fixture
def project():
    taiga_project = f.create_project()
    project = f.TrackingProjectFactory(project=taiga_project)
    project.save()
    return project


@pytest.fixture
def invite(project):
    invite = f.UsersInviteFactory(project=project)
    invite.save()
    return invite

@pytest.fixture
def tracking_project():
    project = f.ProjectFactory()
    track_project = f.TrackingProjectFactory(project=project)
    track_project.save()
    return track_project
