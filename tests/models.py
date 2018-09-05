from auth_backend.user.models import User


class TestUser(User):

    def has_permission(self, code):
        return True
