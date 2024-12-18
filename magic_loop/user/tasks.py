from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_sign_up_mail(email: str, username: str):
    return send_mail(
        subject='Welcome to Magic Loop!',
        message=(
            f"Hi {username},\n\n"
            "Welcome to Magic Loop! 🎉\n\n"
            "We're absolutely delighted to have you join our community of crochet and knitting enthusiasts. "
            "Once you’ve joined this ✨magical loop✨,"
            "there’s no escaping the inspiration, creativity, and joy that comes with it! 🎀\n\n"
            "Dive into endless patterns, share your projects,"
            "and connect with others who love the craft as much as you do. "
            "Your next masterpiece is just a loop away!✨\n\n"
            "Warmest wishes,\n"
            "The Magic Loop Team"
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
