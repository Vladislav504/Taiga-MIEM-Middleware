from taiga.base.api import serializers
from django.utils.translation import ugettext as _
from taiga.base.fields import Field, MethodField, I18NField

class TrackingProjectsSerializer(serializers.LightSerializer):
    number = Field()
    taiga_id = Field(attr='project_id')
    fullname = Field()
