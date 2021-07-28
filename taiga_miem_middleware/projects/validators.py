from django.utils.translation import ugettext as _

from taiga.base.api import validators
from taiga.base.exceptions import ValidationError

from .models import TrackingProjects


class TrackingProjectsValidatior(validators.ModelValidator):
    class Meta:
        model = TrackingProjects
        read_only_fields = ('project', )

    def validate_number(self, attrs, source):
        if self.object is not None and self.object.number != attrs['number']:
            raise ValidationError(_("Invalid Operation. \
                Number of project cannot be changed."))
        return attrs
