from django.core.management.base import BaseCommand, CommandParser, CommandError
from taiga.projects.models import Project

from taiga_miem_middleware.projects.models import TrackingProjects


class Command(BaseCommand):
    help = 'Export Taiga projects to tracking projects'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-project_numbers', nargs='+', type=int)
        parser.add_argument(
            '--all',
            dest='all',
            action='store_false',
            help='Export all tracking projects rather then by numbers')

    def handle(self, *args, **options):
        if options['all']:
            self.export_all()
            return
        list = options['project_numbers'] or []
        self.export_from_list(list)

    def export_all(self):
        for project in Project.objects.all():
            if project.slug.isnumeric():
                self.create_tracking_project(project)

    def export_from_list(self, list):
        for number in list:
            try:
                project = Project.objects.get(slug=str(number))
                self.create_tracking_project(project)
            except Project.DoesNotExist:
                raise CommandError(
                    f"Project with number {number} does not exists!")

    def create_tracking_project(self, project: Project):
        try:
            TrackingProjects.objects.get(project=project)
        except TrackingProjects.DoesNotExist:
            TrackingProjects(project=project,
                             number=int(project.slug),
                             fullname=project.name).save()
