from django.db import models

from taiga.projects.models import Project
from django.utils.translation import ugettext as _


class TrackingProjects(models.Model):
    project = models.OneToOneField(Project,
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   verbose_name=_('tracked_project'))
    number = models.IntegerField(null=False, blank=False, unique=True)
    fullname = models.CharField(max_length=250,
                                null=False,
                                blank=False,
                                verbose_name=_("tracked_project_name"))

    def save(self, *args, **kwargs):
        if self.id != self.number:
            self.id = self.number
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "tracking_project"
        verbose_name_plural = "tracking_projects"
        ordering = [
            'number',
        ]
