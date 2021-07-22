from settings.local import *

DEBUG = True
TEMPLATES[0]["OPTIONS"][
    'context_processors'] += "django.template.context_processors.debug"
ENABLE_TELEMETRY = False

SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False
CELERY_ALWAYS_EAGER = True
CELERY_ENABLED = False

MEDIA_ROOT = "/tmp"
INSTALLED_APPS = list(
    set(INSTALLED_APPS) -
    set(["taiga.hooks.github", "taiga.hooks.gitlab", "taiga.hooks.bitbucket"]))
