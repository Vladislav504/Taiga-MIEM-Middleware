from taiga.base.api.permissions import IsSuperUser, AllowAny
from taiga.base.api.permissions import TaigaResourcePermission


class LeadershipsPermission(TaigaResourcePermission):
    create_perms = IsSuperUser()
    retrieve_perm = AllowAny()
    update_perms = IsSuperUser()