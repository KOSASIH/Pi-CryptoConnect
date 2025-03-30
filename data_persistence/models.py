from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import json

class StateChange(models.Model):
    """A class representing a state change."""

    entity_id = models.CharField(max_length=100, db_index=True)
    entity_type = models.CharField(max_length=100, db_index=True)
    state = models.JSONField()
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='state_changes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']  # Order by timestamp descending
        unique_together = ('entity_id', 'entity_type', 'timestamp')  # Ensure uniqueness

    def __str__(self):
        """Return a string representation of the state change."""
        return f"{self.entity_type} {self.entity_id} - {self.timestamp}"

    def clean(self):
        """Custom validation for the state change."""
        if not self.entity_id or not self.entity_type:
            raise ValidationError("Entity ID and Entity Type cannot be empty.")
        if not isinstance(self.state, dict):
            raise ValidationError("State must be a valid JSON object.")

    def save(self, *args, **kwargs):
        """Override save method to include custom validation."""
        self.clean()  # Call the clean method to validate
        super().save(*args, **kwargs)  # Call the original save method

    @classmethod
    def get_recent_changes(cls, entity_id, entity_type, limit=10):
        """Get the most recent state changes for a specific entity.

        Args:
            entity_id (str): The ID of the entity.
            entity_type (str): The type of the entity.
            limit (int): The maximum number of changes to retrieve.

        Returns:
            QuerySet: A queryset of the most recent state changes.
        """
        return cls.objects.filter(entity_id=entity_id, entity_type=entity_type)[:limit]

    @classmethod
    def get_changes_in_timeframe(cls, entity_id, entity_type, start_time, end_time):
        """Get state changes for a specific entity within a given timeframe.

        Args:
            entity_id (str): The ID of the entity.
            entity_type (str): The type of the entity.
            start_time (datetime): The start of the timeframe.
            end_time (datetime): The end of the timeframe.

        Returns:
            QuerySet: A queryset of state changes within the timeframe.
        """
        return cls.objects.filter(
            entity_id=entity_id,
            entity_type=entity_type,
            timestamp__range=(start_time, end_time)
        )

    def get_state_as_json(self):
        """Return the state as a JSON string."""
        return json.dumps(self.state)

    @property
    def is_recent(self):
        """Check if the state change is recent (within the last hour)."""
        return timezone.now() - self.timestamp < timezone.timedelta(hours=1)
