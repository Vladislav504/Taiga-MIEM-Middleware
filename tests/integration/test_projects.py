import json
import pytest
from django.urls import reverse
from django.apps import apps

from ..utils import signals_switch

pytestmark = pytest.mark.django_db(transaction=True)

# отключаем сигналы, чтобы не было ошибок ProjectTemplateDoesNotExists
disconnect, _ = signals_switch()
disconnect()


def test_successfull_tracking_project_creation(admin_client):
    project_model = apps.get_model("projects", "Project")
    url = reverse('tracking_projects-list')
    data = {"number": 111, "fullname": "111 TEST"}
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 201
    assert response.data['number'] == 111
    assert response.data['fullname'] == "111 TEST"
    assert project_model.objects.filter(slug="111",
                                        name="111 TEST").count() == 1
    assert response.data['taiga_id'] == 1


def test_tracking_project_creation_without_fullname(admin_client):
    url = reverse('tracking_projects-list')
    data = {"number": 111}
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 400


def test_tracking_project_creation_without_number(admin_client):
    url = reverse('tracking_projects-list')
    data = {"fullname": "111 TEST"}
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 400
