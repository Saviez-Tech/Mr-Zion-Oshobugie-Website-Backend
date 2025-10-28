from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Book,Course,Payment
from .serializers import BookSerializer,CourseSerializer,CourseDetailSerializer,ContactMessageSerializer,StrategyCallSerializer,SpeakerInvitationSerializer
from .utils import create_stripe_checkout_session
import stripe
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def get_books(request):
    """
    Returns a list of all books in the database.
    """
    books = Book.objects.all().order_by('-created_at')
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_courses(request):
    """
    Returns a summarized list of all courses.
    """
    courses = Course.objects.all().order_by('-created_at')
    serializer = CourseSerializer(courses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def course_detail(request, course_id):
    try:
        course = Course.objects.prefetch_related('lessons').get(id=course_id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CourseDetailSerializer(course)
    return Response(serializer.data)



@api_view(['POST'])
def create_contact_message(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Your message has been received successfully."},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def book_strategy_call(request):
    serializer = StrategyCallSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Your strategy call has been booked successfully."},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def invite_speaker(request):
    """
    Endpoint to invite Mr. Zion to speak at an event.
    """
    serializer = SpeakerInvitationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Invitation request submitted successfully."},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def access_course(request):
    """
    Endpoint to access a course by its access code.
    """
    access_code = request.data.get('access_code')

    if not access_code:
        return Response(
            {"error": "Access code is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        course = Course.objects.get(access_code=access_code)
    except Course.DoesNotExist:
        return Response(
            {"error": "Invalid access code."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CourseDetailSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def create_payment(request):
    """
    Unified payment endpoint for services, books, and courses.
    - Books/Courses: item_id provided, lookup from DB
    - Services: frontend sends item_name and amount directly
    """
    try:
        data = request.data
        payment_type = data.get('payment_type')  # "book", "course", or "service"
        full_name = data.get('full_name')
        email = data.get('email')
        phone = data.get('phone', None)

        if not payment_type:
            return Response({'error': 'Payment type is required.'}, status=status.HTTP_400_BAD_REQUEST)

        item_name = None
        amount = None
        item_id = data.get('item_id', None)

        # --- BOOK ---
        if payment_type == 'book':
            try:
                item = Book.objects.get(id=item_id)
                item_name = item.title
                amount = item.price
            except Book.DoesNotExist:
                return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        # --- COURSE ---
        elif payment_type == 'course':
            try:
                item = Course.objects.get(id=item_id)
                item_name = item.title
                amount = item.price
            except Course.DoesNotExist:
                return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        # --- SERVICE (STATIC) ---
        elif payment_type == 'service':
            item_name = data.get('item_name')
            amount = data.get('amount')

            if not item_name or not amount:
                return Response(
                    {'error': 'For services, both item_name and amount are required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response({'error': 'Invalid payment type.'}, status=status.HTTP_400_BAD_REQUEST)

        # --- CREATE Payment record ---
        payment = Payment.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            payment_type=payment_type,
            item_id=item_id,
            item_name=item_name,
            amount=amount,
        )

        success_url = f"{settings.SITE_URL}/payment-success"
        cancel_url = f"{settings.SITE_URL}/payment-cancel"

        session = create_stripe_checkout_session(
            amount=amount,
            email=email,
            success_url=success_url,
            cancel_url=cancel_url,
            product_name=item_name,
        )

        payment.payment_id = session.id
        payment.save()

        return Response({'checkout_url': session.url}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['POST'])
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        # Verify event signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

    # Handle successful checkout
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_id = session.get('id')

        payment = Payment.objects.filter(payment_id=payment_id).first()
        if payment:
            payment.status = 'success'
            payment.save()
            return Response({'message': 'Payment updated successfully'}, status=status.HTTP_200_OK)

    # Handle payment failure
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        payment_id = session.get('id')

        payment = Payment.objects.filter(payment_id=payment_id).first()
        if payment:
            payment.status = 'expired'
            payment.save()

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        payment_id = session.get('id')

        payment = Payment.objects.filter(payment_id=payment_id).first()
        if payment:
            payment.status = 'failed'
            payment.save()

    return Response(status=status.HTTP_200_OK)