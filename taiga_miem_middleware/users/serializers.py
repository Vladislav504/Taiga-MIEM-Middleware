from taiga.base.api import serializers
from taiga.base.fields import Field, MethodField


class LeadershipsSerializer(serializers.LightSerializer):
    id = Field()
    project = Field(attr="project_id")
    user = Field(attr="user_id", required=False)
    email = Field()
    is_leader = Field()
    role = Field(attr="role_id")

