import uuid
from django.db import models
from django.conf import settings

from taiga.users.models import Role
from taiga.projects.models import Membership
from taiga.projects.services import send_invitation

from ..projects.models import TrackingProjects


class Leaderships(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             default=None)
    project = models.ForeignKey(TrackingProjects,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False)
    email = models.EmailField(null=False, blank=False)
    is_leader = models.BooleanField(default=False)
    role = models.ForeignKey(Role,
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False)

    class Meta:
        unique_together = (
            'email',
            'project',
        )

    def invite(self):
        data = {
            "project_id": self.project.project_id,
            "is_admin": self.is_leader,
            "role_id": self.role.id
        }
        if self.user is None:
            data['email'] = self.email
            data['token'] = str(uuid.uuid1())
        else:
            data['user_id'] = self.user.id
        membership = Membership(**data)
        membership.save()
        send_invitation(membership)

    def change_membership(self, *args, **kwargs):
        self.update_membership(*args, **kwargs)

    def update_membership(self, membership, new_email=None, new_role=None):
        updated = ["is_admin"]
        membership.is_admin = self.is_leader
        if new_role is not None:
            membership.role = new_role
            updated.append("role")
        if new_email is not None:
            membership.email = new_email
            membership.token = str(uuid.uuid1())
            updated.append("email")
            updated.append("token")
            send_invitation(membership)
        membership.save(update_fields=updated)
