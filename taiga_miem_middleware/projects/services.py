from taiga.projects.models import Project


def create_taiga_project(user, fullname: str, number: int):
    project = Project(owner=user,
                      slug=str(number),
                      name=fullname,
                      description="Empty description")
    project.save()
    return project