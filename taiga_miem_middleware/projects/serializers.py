from taiga.base.api import serializers
from taiga.base.fields import Field


class TrackingProjectsSerializer(serializers.LightSerializer):
    number = Field()
    taiga_id = Field(attr='project_id')
    fullname = Field()
