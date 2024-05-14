from django.db import models


class User(models.Model):
    """A class representing a user."""

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the user."""
        return self.username


class Role(models.Model):
    """A class representing a user role."""

    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField("Permission")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the role."""
        return self.name


class Permission(models.Model):
    """A class representing a permission."""

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the permission."""
        return self.name
