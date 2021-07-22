import json
import pytest
from django.urls import reverse
from django.apps import apps

from .. import factories as f

pytestmark = pytest.mark.django_db(transaction=True)


def test_invite_already_invited_user(admin_client, project):
    url = reverse("tracking_project_users-list")
    data = {
        "email": "example@example.com",
        "project": project.number,
        "role": "Test Role"
    }
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 201
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 400


def test_creating_membership_in_project_for_not_existing_user(
        admin_client, project):
    membership_model = apps.get_model("projects", "Membership")
    url = reverse("tracking_project_users-list")
    data = {
        "email": "example@example.com",
        "project": project.number,
        "role": "Test Role"
    }
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 201
    query = membership_model.objects.filter(email=data['email'],
                                            project=project.project)
    assert query.count() == 1
    assert query.first().user is None
    assert query.first().email == data["email"]
    assert query.first().token is not None


def test_creating_membership_in_project_for_existing_user(
        admin_client, just_user, project):
    membership_model = apps.get_model("projects", "Membership")
    url = reverse("tracking_project_users-list")
    data = {
        "email": just_user.email,
        "project": project.number,
        "role": "Test Role"
    }
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 201
    query = membership_model.objects.all()
    assert query.count() == 1
    assert query.first().user == just_user
    assert query.first().token is None


def test_user_successfully_added_to_project(admin_client, just_user, project):
    role_model = apps.get_model("users", "Role")
    url = reverse("tracking_project_users-list")
    data = {
        "project": project.number,
        "email": just_user.email,
        "role": "Test Role"
    }
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 201
    assert response.data['project'] == project.number
    assert response.data['user'] == just_user.id
    assert response.data['email'] == just_user.email
    assert not response.data['is_leader']
    assert role_model.objects.filter(
        pk=response.data['role']).first().name == "Test Role"


def test_adding_user_without_role(admin_client, just_user, project):
    url = reverse("tracking_project_users-list")
    data = {"email": just_user.email, "project": project.number}
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 400


def test_adding_user_without_email(admin_client, project):
    url = reverse("tracking_project_users-list")
    data = {"role": "test", "project": project.number}
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 400


def test_adding_user_without_project(admin_client, just_user):
    url = reverse("tracking_project_users-list")
    data = {"email": just_user.email, "role": "test"}
    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 400


def test_adding_leader(admin_client, just_user, project):
    url = reverse("tracking_project_users-list")
    data = {
        "email": just_user.email,
        "project": project.number,
        "role": "Test Role",
        "is_leader": True
    }

    response = admin_client.json.post(url, json.dumps(data))
    assert response.status_code == 201
    assert response.data['is_leader']


def test_invitation_change(admin_client, invite):
    url = reverse("tracking_project_users-detail", kwargs={'pk': invite.pk})
    data = {"is_leader": not invite.is_leader, "email": "example@example.com"}
    response = admin_client.json.patch(url, json.dumps(data))
    assert response.status_code == 200


def test_membership_is_admin_change_after_invite_change(admin_client, invite):
    url = reverse("tracking_project_users-detail", kwargs={'pk': invite.pk})
    old = f.MembershipFactory(project=invite.project.project,
                              role=invite.role,
                              user=invite.user)
    old.save()
    old = old.is_admin
    membership_model = apps.get_model("projects", "Membership")
    data = {"is_leader": not old}
    responce = admin_client.json.patch(url, json.dumps(data))
    new = membership_model.objects.get(project=invite.project.project,
                                       user=invite.user)
    new = new.is_admin
    assert responce.status_code == 200
    assert old != new


def test_membership_email_change_after_invite_change(admin_client):
    invite = f.UsersInviteFactory(user=None, email="example@example.com")
    invite.save()
    url = reverse("tracking_project_users-detail", kwargs={'pk': invite.pk})
    old = f.InvitationFactory(project=invite.project.project,
                              role=invite.role,
                              email=invite.email)
    old.save()
    membership_model = apps.get_model("projects", "Membership")
    data = {"email": "new@example.com"}
    responce = admin_client.json.patch(url, json.dumps(data))
    new = membership_model.objects.get(project=invite.project.project,
                                       email=data['email'])
    assert responce.status_code == 200
    assert old.token != new.token
    assert old.email != new.email


def test_membership_deleted_after_existed_user_invite_deletion(
        admin_client, invite):
    url = reverse("tracking_project_users-detail", kwargs={'pk': invite.pk})
    f.InvitationFactory(project=invite.project.project,
                        role=invite.role,
                        user=invite.user).save()
    membership_model = apps.get_model("projects", "Membership")
    response = admin_client.json.delete(url)
    assert response.status_code == 204
    assert membership_model.objects.filter(project=invite.project.project,
                                           user=invite.user).count() == 0


def test_membership_deleted_after_not_existed_user_invite_deletion(
        admin_client):
    invite = f.UsersInviteFactory(user=None, email="example@example.com")
    invite.save()
    url = reverse("tracking_project_users-detail", kwargs={'pk': invite.pk})
    f.InvitationFactory(project=invite.project.project,
                        role=invite.role,
                        email=invite.email).save()
    membership_model = apps.get_model("projects", "Membership")
    response = admin_client.json.delete(url)
    assert response.status_code == 204
    assert membership_model.objects.filter(project=invite.project.project,
                                           user=invite.user).count() == 0

