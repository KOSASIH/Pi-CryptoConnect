from django.db import models

class StateChange(models.Model):
    """A class representing a state change."""

    entity_id = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=100)
    state = models.JSONField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the state change."""
        return f"{self.entity_type} {self.entity_id} - {self.timestamp}"
