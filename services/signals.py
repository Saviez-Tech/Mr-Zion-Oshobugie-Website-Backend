from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Payment, Course, Book
from .email_helper import send_course_payment_email, send_book_payment_email,send_service_payment_email


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
    """
    Sends the correct email when a payment transitions to 'success'.
    Uses helper functions for clean structure.
    """
    # Only trigger when status changes to 'success'
    if getattr(instance, "_previous_status", None) != "success" and instance.status.lower() == "success":
        try:
            if instance.payment_type == "course":
                # ✅ Fetch course details
                course = Course.objects.filter(id=instance.item_id).first()
                if course:
                    course_link = f"https://yourfrontenddomain.com/courses/{course.id}"
                    access_code = course.access_code

                    # 👇 Use your helper function to send email
                    send_course_payment_email(
                        email=instance.email,
                        full_name=instance.full_name,
                        course_title=course.title,
                        access_code=access_code,
                        course_link=course_link
                    )
                    print(f"✅ Course payment email sent to {instance.email}")

            elif instance.payment_type == "book":
                book = Book.objects.filter(id=instance.item_id).first()
                if book:
                    book_links = {
                        "Kindle": book.kindle_link,
                        "Paperback": book.paperback_link,
                        "PDF": book.pdf_link,
                    }
                    send_book_payment_email(
                        email=instance.email,
                        full_name=instance.full_name,
                        book_title=book.title,
                        book_links=book_links
                    )

            elif instance.payment_type == "service": 
                send_service_payment_email(
                    email=instance.email,
                    full_name=instance.full_name,
                    service_name=instance.item_name
                )

        except Exception as e:
            print(f"❌ Failed to send success email for {instance.email}: {e}")
