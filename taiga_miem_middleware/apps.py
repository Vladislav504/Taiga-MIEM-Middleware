from django.apps import AppConfig
from django.conf.urls import include, url


class TaigaMiemMiddlewareConfig(AppConfig):
    name = 'taiga_miem_middleware'

    def ready(self):
        from taiga.urls import urlpatterns
        from .urls import patterns_urls
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
