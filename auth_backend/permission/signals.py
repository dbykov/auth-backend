from django.dispatch import Signal

# Сигнал, отправляемый после завершения формирования разрешений в БД
after_create_permissions = Signal()
