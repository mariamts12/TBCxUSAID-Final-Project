from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_pattern_saved_email(
    pattern_title: str, user_email: str, username: str, saved_count: int
):
    return send_mail(
        subject=f"Your pattern '{pattern_title}' has reached {saved_count} saves!",
        message=(
            f"Dear {username},\n\n"
            f"Your pattern titled '{pattern_title}' has received {saved_count} saves! 🎉"
            f"Congratulations on reaching this milestone!✨\n\n"
            f"Best wishes,\n"
            "The Magic Loop Team"
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
    )
