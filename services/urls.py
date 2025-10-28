from django.urls import path
from .views import *

urlpatterns = [
    path('books/',get_books, name='get_books'),
    path('courses/',get_courses, name='get_courses'),
    path('courses/<int:course_id>/', course_detail, name='course-detail'),

    path('contact/', create_contact_message, name='contact-message'),
    path('strategy-call/', book_strategy_call, name='book-strategy-call'),
    path('invite-speaker/', invite_speaker, name='invite-speaker'),

    path('access-course/', access_course, name='access-course'),

    path('create-payment/', create_payment, name='create-payment'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
