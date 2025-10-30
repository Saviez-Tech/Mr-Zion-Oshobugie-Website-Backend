from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    cover_image = models.URLField()
    kindle_link = models.URLField(blank=True, null=True)
    paperback_link = models.URLField(blank=True, null=True)
    pdf_link = models.URLField(blank=True, null=True)  # Optional direct PDF
    free_chapter_pdf = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    bundle_eligible = models.BooleanField(default=True)
    what_readers_will_learn = models.JSONField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=100)  # e.g. "6 weeks | 12 modules"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor_name = models.CharField(max_length=100, default="Zion Oshiobugie")
    instructor_photo = models.URLField(blank=True, null=True)
    thumbnail = models.URLField()
    what_you_learn = models.TextField()
    who_is_for = models.TextField(blank=True, null=True)
    access_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CourseLesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    resource= models.URLField(blank=True,null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    

from django.db import models


class StrategyCall(models.Model):
    CALL_TYPE_CHOICES = [
        ('ngo', 'NGO Strategy Call'),
        ('cic', 'CIC Strategy Call'),
    ]

    STAGE_CHOICES = [
        ('idea', 'Still an idea'),
        ('registering', 'Currently registering'),
        ('registered', 'Already registered'),
        ('growing', 'Active and growing'),
    ]

    call_type = models.CharField(max_length=10, choices=CALL_TYPE_CHOICES)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=200, blank=True, null=True)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    goal = models.TextField(help_text="What’s your main goal for this session?")
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.call_type.upper()}) - {self.organization_name or 'No Org Name'}"


class SpeakerInvitation(models.Model):
    EVENT_STRUCTURE_CHOICES = [
        ('keynote', 'Keynote Speech'),
        ('panel', 'Panel Discussion'),
        ('podcast', 'Podcast'),
        ('masterclass', 'Masterclass'),
        ('workshop', 'Workshop / Training'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=200)
    event_structure = models.CharField(
        max_length=50,
        choices=EVENT_STRUCTURE_CHOICES,
        help_text="Select the type of event you’re inviting Zion for."
    )
    message = models.TextField(
        help_text="Brief description of your event and audience."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Speaker Invitation"
        verbose_name_plural = "Speaker Invitations"

    def __str__(self):
        return f"{self.full_name} - {self.organization_name} ({self.event_structure})"
    


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('service', 'Service'),
        ('book', 'Book'),
        ('course', 'Course'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    item_id = models.PositiveIntegerField(blank=True, null=True)  # only used for book/course
    item_name = models.CharField(max_length=200)  # name of the service/book/course
    qty=models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")
    satisfied=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.payment_type} - {self.amount}"

class ServicePayment(Payment):
    class Meta:
        proxy = True
        verbose_name = "Service Payment"
        verbose_name_plural = "Service Payments"


class BookPayment(Payment):
    class Meta:
        proxy = True
        verbose_name = "Book Payment"
        verbose_name_plural = "Book Payments"


class CoursePayment(Payment):
    class Meta:
        proxy = True
        verbose_name = "Course Payment"
        verbose_name_plural = "Course Payments"