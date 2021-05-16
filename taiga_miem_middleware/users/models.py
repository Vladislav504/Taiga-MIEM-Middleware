from django.db import models
from django.conf import settings

from taiga.users.models import User
from taiga.projects.models import Project


class Leaderships(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                default=None)
    project_id = models.ForeignKey(Project,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   blank=False)
    email = models.EmailField(null=False, blank=False)

    class Meta:
        unique_together = (('project_id', 'email'), )
