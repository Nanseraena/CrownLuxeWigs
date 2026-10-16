import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _send(subject, recipient, template_name, context):
    """Send a branded multipart email without allowing email failures to break checkout/auth."""
    html = render_to_string(template_name, context)
    message = EmailMultiAlternatives(subject, "Please view this email in an HTML-capable email client.", settings.DEFAULT_FROM_EMAIL, [recipient])
    message.attach_alternative(html, "text/html")
    try:
        message.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("Unable to send account email to %s", recipient)
        return False


def send_password_reset_email(user, reset_url):
    return _send(
        "Reset your CrownLuxe password",
        user.email,
        "emails/password_reset.html",
        {"user": user, "reset_url": reset_url},
    )


def send_welcome_email(user):
    return _send(
        "Welcome to CrownLuxe",
        user.email,
        "emails/welcome.html",
        {"user": user, "store_url": settings.FRONTEND_URL},
    )
