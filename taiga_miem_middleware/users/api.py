from taiga.base.api import ModelCrudViewSet
from taiga.projects.models import Membership
from taiga.projects.services.members import remove_user_from_project

from .serializers import LeadershipsSerializer
from .validators import LeadershipsValidatior
from .permissions import LeadershipsPermission
from .models import Leaderships


class UsersViewSet(ModelCrudViewSet):
    serializer_class = LeadershipsSerializer
    validator_class = LeadershipsValidatior
    permission_classes = (LeadershipsPermission, )
    model = Leaderships

    def post_save(self, obj, created=False):
        if created:
            membership = Membership.objects.filter(project=obj.project.project)
            try:
                if obj.user is not None:
                    membership = membership.get(user=obj.user)
                else:
                    membership = membership.get(email=obj.email)
                obj.change_membership(membership, new_role=obj.role)
            except Membership.DoesNotExist:
                obj.invite()

    def pre_delete(self, obj):
        try:
            if obj.user is not None:
                remove_user_from_project(obj.user, obj.project.project)
            else:
                Membership.objects.get(email=obj.email,
                                       project=obj.project.project).delete()
        finally:
            pass
