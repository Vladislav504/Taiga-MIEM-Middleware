from taiga.base.api import ModelCrudViewSet

from .models import Leaderships

class UsersViewSet(ModelCrudViewSet):
    model = Leaderships
