from django import dispatch
from .models import Leaderships
from ..projects.models import TrackingProjects


def update_leadership_user(sender, instance, created, update_fields, **kwargs):
    if created or update_fields is None or 'user' not in update_fields:
        return
    track_project = TrackingProjects.objects.get(project=instance.project)
    query = Leaderships.objects.filter(project=track_project)
    if instance.user is not None:
        leadership = query.get(email=instance.email)
        leadership.user = instance.user
        leadership.save(update_fields=["user"])
