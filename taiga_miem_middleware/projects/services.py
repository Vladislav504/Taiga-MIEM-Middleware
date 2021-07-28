from django.db.models.query_utils import Q
from taiga.projects.models import Project


def create_taiga_project(user, fullname: str, number: int):
    project = Project(owner=user,
                      slug=str(number),
                      name=fullname,
                      description="Empty description",
                      is_private=False)
    project.save()
    return project


def find_existing_project(number):
    return Project.objects.get(slug=str(number))
    