from django.db.models import Manager

from auth_backend.base.utils import get_active_organization_id


class ByOrganizationManager(Manager):
    """
    Менеджер, добавляющий фильтр по текущей активной организации
    """

    def get_queryset(self):
        queryset = super(ByOrganizationManager, self).get_queryset()

        current_organization_id = get_active_organization_id()
        if current_organization_id is not None:
            queryset = queryset.filter(organization=current_organization_id)
        else:
            queryset = queryset.all()

        return queryset
