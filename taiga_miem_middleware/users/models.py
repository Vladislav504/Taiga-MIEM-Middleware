import uuid
from django.db import models
from django.db.models import Q
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

    def change_membership(self):
        membership = Membership.objects.get(
            Q(user=self.user), Q(project=self.project.project))
        membership.is_admin = self.is_leader
        membership.save(update_fields=["is_admin"])

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