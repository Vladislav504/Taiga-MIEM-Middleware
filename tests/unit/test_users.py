import pytest

from taiga.auth.services import accept_invitation_by_existing_user

from taiga_miem_middleware.users.models import Leaderships
from .. import factories as f

pytestmark = pytest.mark.django_db(transaction=True)

def test_user_accept_invite():
    invite = f.UsersInviteFactory(user=None, email="example@example.com")
    membership = f.InvitationFactory(project=invite.project.project,
                                     role=invite.role,
                                     email=invite.email)
    user = f.UserFactory(email="another@email.com")
    membership.save()
    invite.save()
    user.save()
    accept_invitation_by_existing_user(membership.token, user.id)
    invite = Leaderships.objects.get(project=invite.project,
                                     email=membership.email)
    assert invite.user is not None
