from taiga.base.api import validators
from taiga.base.api import serializers
from taiga.base.exceptions import ValidationError
from taiga.projects.models import Membership, Project
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
        """
        Нельзя изменить Leadership с уже существующим проектом,
        если изменыемый и новый проекты совпадают, то изменение возможно
        """
        if self.object is not None and self.object.project != attrs['project']:
            raise ValidationError(_("Invalid Operation"))
        if attrs.get('project', None) is None:
            raise ValidationError(_("Please specify project number!"))
        return attrs

    def validate_is_leader(self, attrs, source):
        if self.object is not None:
            self.change_membership = True
        return attrs

    def validate_email(self, attrs, source):
        """
        Находим пользователя при создании Leadership.
        При его изменении, если пользователя еще не существует,
        будет изменяться Membership проекта, если же он
        существует, то меняется только Leadership.
        """
        if self.object is not None:
            if self.object.user is None:
                self.change_membership = True
                self.old_email = self.object.email
            return attrs
        user = User.objects.filter(email=attrs["email"]).first()
        if user is not None:
            self.user = user
        return attrs

    def validate_role(self, attrs, source):
        """
        Роль не должна меняться. Создается новая роль для каждого пользователя.
        """
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

        # устанваливаем найденного пользователя
        if hasattr(self, "user") and self.object is not None:
            self.object.user = self.user

        # если нужно изменить приглашение
        if hasattr(self, "change_membership"
                   ) and self.object is not None and self.change_membership:
            self._change_membership()

        return errors

    def _change_membership(self):
        """
        Изменяем email существующего приглашения пользователя
        в проект по измененному Leadership
        """
        email = self.object.email
        new_email = self.object.email
        project = self.object.project.project

        if hasattr(self, "old_email"):
            email = self.old_email

        membership = Membership.objects.filter(project=project)
        if self.object.user is not None:
            membership = membership.filter(user=self.object.user)
        else:
            membership = membership.filter(email=email)
        if membership.exists():
            membership = membership.first()
            self.object.change_membership(membership, new_email=new_email)
        else:
            self.object.invite()
