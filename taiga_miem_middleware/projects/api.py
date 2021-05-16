from django.db.models import query
from taiga.base.api import ModelCrudViewSet

from .models import TrackingProjects
from .validators import TrackingProjectsValidatior
from .serializers import TrackingProjectsSerializer
from .services import create_taiga_project
from . import permissions


class TrackingProjectsViewSet(ModelCrudViewSet):
    model = TrackingProjects
    validator_class = TrackingProjectsValidatior
    serializer_class = TrackingProjectsSerializer
    permission_classes = (permissions.TrackingProjectsPermission, )
    queryset = TrackingProjects.objects.all()

    ordering = ("number", )

    def post_save(self, obj, created=False):
        if created:
            project = create_taiga_project(self.request.user, obj.fullname,
                                           obj.number)
            tracking_record = self.queryset.get(id=obj.id)
            tracking_record.project = project
            tracking_record.save(update_fields=['project'])
