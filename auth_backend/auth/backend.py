from django.contrib.auth.backends import ModelBackend


class AuthenticationBackend(ModelBackend):

    def has_perm(self, user_obj, perm, obj=None):
        result = super(
            AuthenticationBackend, self
        ).has_perm(user_obj, perm, obj)

        return True
