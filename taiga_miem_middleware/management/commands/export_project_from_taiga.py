from django.core.management.base import BaseCommand
from taiga.projects.models import Project

from taiga_miem_middleware.projects.models import TrackingProjects


class Command(BaseCommand):
    help = 'Export Taiga projects to tracking projects'

    def handle(self, *args, **options):
        for project in Project.objects.all():
            if project.slug.isnumeric():
                try:
                    TrackingProjects.objects.get(project=project)
                except TrackingProjects.DoesNotExist:
                    TrackingProjects(project=project,
                                     number=int(project.slug),
                                     fullname=project.name).save()
