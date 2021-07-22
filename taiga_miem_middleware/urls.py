from dataclasses import dataclass
from typing import Any

from .projects.api import TrackingProjectsViewSet
from .users.api import UsersViewSet


@dataclass
class URLPattern:
    url: str
    view: Any
    base_name: str


patterns_urls = [
    URLPattern('projects', TrackingProjectsViewSet, "tracking_projects"),
    URLPattern('users', UsersViewSet, "tracking_project_users"),
]
