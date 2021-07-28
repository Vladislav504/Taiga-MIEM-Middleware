from taiga.base.api import ModelCrudViewSet
from taiga.projects.models import Project
from taiga.projects.services.projects import delete_project

from .models import TrackingProjects
from .validators import TrackingProjectsValidatior
from .serializers import TrackingProjectsSerializer
from .services import create_taiga_project, find_existing_project
from . import permissions

# изменяемые через апи поля,
# соответствие полей "модель": "проект в Тайге"
updatable_fields = {'fullname': "name"}


class TrackingProjectsViewSet(ModelCrudViewSet):
    model = TrackingProjects
    validator_class = TrackingProjectsValidatior
    serializer_class = TrackingProjectsSerializer
    permission_classes = (permissions.TrackingProjectsPermission, )
    queryset = TrackingProjects.objects.all()

    ordering = ("number", )

    def pre_delete(self, obj):
        delete_project(obj.project.id)
        super().pre_delete(obj)

    def post_save(self, obj, created=False):
        if created:
            self.make_project(obj)
            return
        self.change_project(obj)

    def change_project(self, obj):
        project = obj.project
        for obj_attr, proj_attr in updatable_fields.items():
            obj_value = getattr(obj, obj_attr)
            setattr(project, proj_attr, obj_value)
        project.save(update_fields=updatable_fields.values())

    def make_project(self, obj):
        try:
            project = find_existing_project(obj.number)
        except Project.DoesNotExist:
            project = create_taiga_project(self.request.user, obj.fullname,
                                           obj.number)
        obj.project = project
        obj.save(update_fields=['project'])
