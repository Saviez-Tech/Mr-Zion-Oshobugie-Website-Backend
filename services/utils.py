import stripe
from django.conf import settings
import random
import string


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_checkout_session(amount, email, success_url, cancel_url):
    """
    Create a Stripe Checkout Session.
    Amount should be in kobo/cents (smallest unit).
    """
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(amount * 100),  # Stripe expects amount in cents
                'product_data': {
                    'name': 'Consultation Payment',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        customer_email=email,
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def generate_course_id():
        return "COURSE-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))