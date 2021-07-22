from django.utils.translation import ugettext as _
from taiga.base import exceptions as exc
from taiga.base.api import ModelCrudViewSet
from taiga.projects.models import Membership
from taiga.projects.services import members
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
            obj.invite()
        # TODO: разобраться с изменением приглашения пользователя, 
        # 1) если пользователь уже есть в проекте, изменение email приводит к изменению email только в модели Leaderships, изменение is leader меняет is admin в membership
        # 2) если приглашение пользователя уже есть в проекте, то в membership меняется и email и is leader (или удаляется старое приглашение и создается новое) обязтельно нужно будет высылать приглашние на почту
        # 3) 1 и 2 должны выполняться даже когда Leadership только создается в первый раз
        # if obj.user is None:
        #     Membership.objects.get(email=obj.)

    def pre_delete(self, obj):
        if obj.user is not None:
            remove_user_from_project(obj.user, obj.project)
        else:
            Membership.objects.get(email=obj.user.email,
                                   project=obj.project.project).delete()
