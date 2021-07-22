from taiga.users.models import Role
from taiga.permissions.choices import MEMBERS_PERMISSIONS


def create_role(role_name, project):
    perms = [val[0] for val in MEMBERS_PERMISSIONS]
    role = Role(name=role_name, project=project, permissions=perms)
    role.save()
    return role
