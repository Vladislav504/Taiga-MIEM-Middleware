from taiga.base.api import validators

from .models import TrackingProjects

class TrackingProjectsValidatior(validators.ModelValidator):
    class Meta:
        model = TrackingProjects
        read_only_fields = ('project',)