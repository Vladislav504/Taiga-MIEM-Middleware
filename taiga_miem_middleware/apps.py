from django.apps import AppConfig


class TaigaMiemMiddlewareConfig(AppConfig):
    name = 'taiga_miem_middleware'

    def ready(self):
        print("MIEM Middleware Ready!")