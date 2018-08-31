from auth_backend.base.local import get_thread_data


class ThreadLocalMiddleware:
    """
    Промежуточный слой для реализации сохранения информации
    о пользователе и организации в контексте запроса
    """

    def proccess_request(self, request):
        thread_data = get_thread_data()
        thread_data.user_id = request.user.id

    def process_exception(self, *args, **kwargs):
        self._reset_thread_data()

    def process_response(self, request, response):
        self._reset_thread_data()

    def _reset_thread_data(self):
        thread_data = get_thread_data()
        thread_data.reset()
