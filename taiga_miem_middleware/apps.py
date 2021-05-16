from django.apps import AppConfig
from django.conf.urls import include, url

class TaigaMiemMiddlewareConfig(AppConfig):
    name = 'taiga_miem_middleware'

    def ready(self):
        from taiga.base import routers
        from taiga.urls import urlpatterns

        from .projects.api import TrackingProjectsViewSet
        from .users.api import UsersViewSet

        router = routers.DefaultRouter(trailing_slash=False)
        router.register('projects', TrackingProjectsViewSet, base_name="tracking_projects")
        router.register(r'projects/(?P<resource_id>\d+)/users', UsersViewSet, base_name="project_users")
        
        urlpatterns.append(url(r'^miem/api/', include(router.urls)))
        print("MIEM Middleware Ready!")