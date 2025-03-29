from rest_framework import authentication, exceptions
from .models import User

class UsernamePasswordAuthentication(authentication.BaseAuthentication):
    """A custom authentication class that uses a username and password."""

    def authenticate(self, request):
        """Authenticate the user based on the provided username and password.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            (User, None) if the user is authenticated, (None, None) otherwise.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise exceptions.AuthenticationFailed("Missing username or password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid username or password")

        if user.password != password:
            raise exceptions.AuthenticationFailed("Invalid username or password")

        return (user, None)

def has_permission(user, permission):
    """Check if the user has the specified permission.

    Args:
        user (User): The user to check.
        permission (Permission): The permission to check.

    Returns:
        True if the user has the permission, False otherwise
