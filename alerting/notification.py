import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client  # Twilio for SMS notifications
from your_app.models import AlertRule  # Adjust the import based on your app structure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_email_notification(to, subject, body):
    """Send an email notification.

    Args:
        to (str): The email address to send the notification to.
        subject (str): The subject of the email.
        body (str): The body of the email.
    """
    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT", 587)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to
    msg.attach(MIMEText(body, "html"))  # Support for HTML body

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to, msg.as_string())
        server.quit()
        logging.info("Email notification sent to %s", to)
    except Exception as e:
        logging.error("Error sending email notification: %s", e)

def send_sms_notification(to, message):
    """Send an SMS notification.

    Args:
        to (str): The phone number to send the notification to.
        message (str): The message to send.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to
        )
        logging.info("SMS notification sent to %s", to)
    except Exception as e:
        logging.error("Error sending SMS notification: %s", e)

def check_alert_rules():
    """Check the alert rules and send notifications if necessary."""
    alert_rules = AlertRule.objects.all()

    for alert_rule in alert_rules:
        # Example logic to check if the alert condition is met
        current_value = get_current_value(alert_rule)  # Implement this function based on your logic
        if alert_rule.check_alert(current_value):  # Assuming check_alert is a method in AlertRule
            message = f"Alert: {alert_rule.name} has been triggered. Current value: {current_value}"
            send_email_notification(alert_rule.user.email, "Alert Notification", message)
            send_sms_notification(alert_rule.user.phone_number, message)  # Assuming user has a phone_number field
            logging.info("Notification sent for alert rule: %s", alert_rule.name)

def get_current_value(alert_rule):
    """Fetch the current value based on the alert rule's condition."""
    # Implement logic to retrieve the current value for the alert rule
    # This could involve querying a database, an API, etc.
    return 0  # Placeholder return value
