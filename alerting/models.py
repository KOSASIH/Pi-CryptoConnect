from django.db import models

class AlertRule(models.Model):
    """A class representing an alert rule."""

    name = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    threshold = models.FloatField()
    notification_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the alert rule."""
        return self.name
