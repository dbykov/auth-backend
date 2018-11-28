from django.core.exceptions import ValidationError

from auth_backend.role.utils import READONLY_ROLE_CODES


class ReadOnlyRoleValidator(object):

    message = 'Роль "{field_name}" запрещено редактировать'

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, 'instance', None)

    def __call__(self, *args, **kwargs):
        role_code = getattr(self.instance, 'code', None)
        if role_code in READONLY_ROLE_CODES:
            message = self.message.format(field_name=self.instance.name)
            raise ValidationError(message, code='readOnly')
