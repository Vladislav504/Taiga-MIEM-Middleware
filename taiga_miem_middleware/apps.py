from django.apps import AppConfig
from django.conf.urls import include, url
from django.db.models import signals
from django.apps import apps


class TaigaMiemMiddlewareConfig(AppConfig):
    name = 'taiga_miem_middleware'

    def connect_signals(self):
        self.connect_user_signals()

    def connect_user_signals(self):
        from .users import handlers
        signals.post_save.connect(handlers.update_leadership_user,
                                  sender=apps.get_model(
                                      "projects", "Membership"),
                                  dispatch_uid="update_leadership_user")

    def ready(self):
        from taiga.urls import urlpatterns
        from .urls import patterns_urls
        self.connect_signals()
        router = register_urls(patterns_urls)
        urlpatterns.append(url(r'^miem/api/', include(router.urls)))
        print("MIEM Middleware Ready!")


def register_urls(patterns_urls):
    """
    Register urls in Taiga router
    """
    from taiga.base import routers

    router = routers.DefaultRouter(trailing_slash=False)
    for pattern_url in patterns_urls:
        router.register(pattern_url.url,
                        pattern_url.view,
                        base_name=pattern_url.base_name)
    return router
