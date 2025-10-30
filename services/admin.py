from django.contrib import admin
from .models import Book,Course,CourseLesson,ContactMessage,StrategyCall,SpeakerInvitation,Payment

# Register your models here.

admin.site.register(Book)
admin.site.register(ContactMessage)
admin.site.register(StrategyCall)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "payment_type",
        "item_name",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("payment_type", "status", "created_at")
    search_fields = ("full_name", "email", "item_name", "payment_id")
    readonly_fields = ("created_at", "payment_id")
    ordering = ("-created_at",)
    fieldsets = (
        ("Customer Info", {
            "fields": ("full_name", "email", "phone")
        }),
        ("Payment Details", {
            "fields": ("payment_type", "item_id", "item_name", "amount", "status")
        }),
        ("Stripe Info", {
            "fields": ("payment_id",)
        }),
        ("Timestamps", {
            "fields": ("created_at",),
        }),
    )

@admin.register(SpeakerInvitation)
class SpeakerInvitationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'phone_number', 'organization_name',
        'event_structure', 'country', 'created_at'
    )
    list_filter = ('event_structure', 'country', 'created_at')
    search_fields = ('full_name', 'email', 'organization_name', 'country')
    ordering = ('-created_at',)

class CourseLessonInline(admin.TabularInline):  # or admin.StackedInline for bigger forms
    model = CourseLesson
    extra = 1  # show one empty form for quick add
    fields = ('title', 'video_url', 'resource','order')
    ordering = ('order',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'price', 'instructor_name', 'created_at')
    search_fields = ('title', 'description', 'instructor_name')
    list_filter = ('created_at',)
    inlines = [CourseLessonInline]