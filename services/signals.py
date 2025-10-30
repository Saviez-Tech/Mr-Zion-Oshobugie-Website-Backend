from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment


@receiver(pre_save, sender=Payment)
def store_previous_status(sender, instance, **kwargs):
    """Temporarily store the old status to detect changes."""
    if instance.pk:
        try:
            old_instance = Payment.objects.get(pk=instance.pk)
            instance._previous_status = old_instance.status
        except Payment.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Payment)
def send_payment_success_email(sender, instance, created, **kwargs):
    """Send email once status changes to success."""
    # Only send when updated from non-success to success
    if getattr(instance, "_previous_status", None) != "success" and instance.status.lower() == "success":
        subject = ""
        message = ""

        if instance.payment_type == "service":
            print("service")
            subject = "Your Service Payment Was Successful!"
            message = f"Hi {instance.full_name},\n\nThank you for paying for our service: {instance.item_name}.\nYour payment of ₦{instance.amount} was successful.\n\nWe'll contact you shortly with next steps.\n\n– Team"
        
        elif instance.payment_type == "book":
            print("service")
            subject = "Your Book Purchase Was Successful!"
            message = f"Hi {instance.full_name},\n\nThank you for purchasing the book: {instance.item_name}.\nYour payment of ₦{instance.amount} was successful.\n\nCheck your email shortly for download/access details.\n\n– Team"
        
        elif instance.payment_type == "course":
            print("service")
            subject = "Your Course Payment Was Successful!"
            message = f"Hi {instance.full_name},\n\nThank you for enrolling in the course: {instance.item_name}.\nYour payment of ₦{instance.amount} was successful.\n\nYou’ll get access instructions soon.\n\n– Team"

        if subject and message:
            send_mail(
                subject,
                message,
                getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
                [instance.email],
                fail_silently=True,
            )
