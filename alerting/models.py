from django.db import models
from django.contrib.auth.models import User
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AlertRule(models.Model):
    """A class representing an alert rule."""

    name = models.CharField(max_length=100)
    condition = models.JSONField()  # Store complex conditions as JSON
    threshold = models.FloatField()
    notification_type = models.CharField(max_length=50, choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_rules')  # Associate with a user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the alert rule."""
        return self.name

    def validate_condition(self):
        """Validate the condition format."""
        try:
            json.loads(self.condition)
            return True
        except json.JSONDecodeError:
            logging.error(f"Invalid condition format for alert rule: {self.name}")
            return False

    def check_alert(self, current_value):
        """Check if the alert condition is met."""
        if not self.validate_condition():
            return False

        # Example of condition checking logic
        condition_type = self.condition.get('type')
        if condition_type == 'greater_than':
            return current_value > self.threshold
        elif condition_type == 'less_than':
            return current_value < self.threshold
        elif condition_type == 'equal_to':
            return current_value == self.threshold
        else:
            logging.error(f"Unknown condition type: {condition_type} for alert rule: {self.name}")
            return False

    def send_notification(self, message):
        """Send notification based on the notification type."""
        if self.notification_type == 'email':
            self.send_email(message)
        elif self.notification_type == 'sms':
            self.send_sms(message)
        elif self.notification_type == 'push':
            self.send_push_notification(message)

    def send_email(self, message):
        """Placeholder for sending an email notification."""
        logging.info(f"Sending email to {self.user.email}: {message}")

    def send_sms(self, message):
        """Placeholder for sending an SMS notification."""
        logging.info(f"Sending SMS to {self.user.phone_number}: {message}")

    def send_push_notification(self, message):
        """Placeholder for sending a push notification."""
        logging.info(f"Sending push notification to {self.user.username}: {message}")

# Admin customization (in admin.py)
from django.contrib import admin

@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'condition', 'threshold', 'notification_type', 'created_at', 'updated_at')
    search_fields = ('name', 'user__username', 'condition')
    list_filter = ('notification_type', 'created_at')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        """Override save method to log alert rule creation."""
        super().save_model(request, obj, form, change)
        if not change:
            logging.info(f"Alert rule created: {obj.name} by user: {request.user.username}")
        else:
            logging.info(f"Alert rule updated: {obj.name} by user: {request.user.username}")
