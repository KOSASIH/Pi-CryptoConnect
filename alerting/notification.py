import smtplib
from email.mime.text import MIMEText


def send_email_notification(to, subject, body):
    """Send an email notification.

    Args:
        to (str): The email address to send the notification to.
        subject (str): The subject of the email.
        body (str): The body of the email.
    """
    from_email = "alerting@example.com"
    password = "password"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to

    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to, msg.as_string())
        server.quit()
        print("Email notification sent")
    except Exception as e:
        print(f"Error sending email notification: {e}")


def send_sms_notification(to, message):
    """Send an SMS notification.

    Args:
        to (str): The phone number to send the notification to.
        message (str): The message to send.
    """
    # TODO: Implement this
    pass


def check_alert_rules():
    """Check the alert rules and send notifications if necessary."""
    alert_rules = AlertRule.objects.all()

    for alert_rule in alert_rules:
        # TODO: Implement this
        pass
