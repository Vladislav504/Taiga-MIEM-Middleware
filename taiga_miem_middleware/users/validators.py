from taiga.base.api import validators
from taiga.base.api import serializers
from taiga.base.exceptions import ValidationError
from taiga.projects.models import Membership, Project
from taiga.projects.services import members
from taiga.users.models import User

from django.utils.translation import ugettext as _

from .models import Leaderships
from .services import create_role


class LeadershipsValidatior(validators.ModelValidator):
    role = serializers.CharField(required=True)

    class Meta:
        model = Leaderships
        read_only_fields = ("user", )

    def validate_project(self, attrs, source):
        if self.object is not None and self.object.project != attrs['project']:
            raise ValidationError(_("Invalid Operation"))
        if attrs.get('project', None) is None:
            raise ValidationError(_("Please specify project number!"))
        return attrs

    def validate_email(self, attrs, source):
        if self.object is not None:
            if self.object.user is None:
                membership = Membership.objects.filter(
                    email=self.object.email,
                    project=self.object.project.project)
                if membership.exists():
                    membership.delete()
            return attrs
        user = User.objects.filter(email=attrs["email"]).first()
        if user is not None:
            self.user = user
        return attrs

    def validate_role(self, attrs, source):
        if self.object is not None and self.object.role != attrs['role']:
            raise ValidationError(_("Invalid Operation"))
        project_number = attrs.get('project', None)
        if project_number is None:
            raise ValidationError(_("Please specify project number!"))
        project = Project.objects.get(pk=attrs['project'].project_id)
        attrs['role'] = create_role(attrs['role'], project)
        return attrs

    def is_valid(self):
        errors = super().is_valid()
        if hasattr(self, "user") and self.object is not None:
            self.object.user = self.user

        return errors
