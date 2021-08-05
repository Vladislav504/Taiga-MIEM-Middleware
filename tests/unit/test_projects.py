import pytest
from django.core.management import call_command

from .. import factories as f
from taiga_miem_middleware.projects.models import TrackingProjects

pytestmark = pytest.mark.django_db(transaction=True)


def test_import_taiga_project():
    taiga_project = f.create_project(slug='111', name="111 Full name")
    call_command('export_project_from_taiga')
    track_project = TrackingProjects.objects.filter(number=111)
    assert track_project.exists()
    assert track_project.first().project == taiga_project


def test_import_taiga_project_with_invalid_name():
    f.create_project(slug='111-1', name="111-1 Incorrect name")
    call_command('export_project_from_taiga')
    query = TrackingProjects.objects.all()
    assert len(query) == 0
