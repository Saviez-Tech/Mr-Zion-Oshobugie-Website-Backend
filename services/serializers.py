from rest_framework import serializers
from .models import Book,Course,CourseLesson,ContactMessage,StrategyCall,SpeakerInvitation

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    modules_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'duration', 'price',
            'thumbnail', 'modules_count', 'created_at'
        ]

    def get_modules_count(self, obj):
        return obj.lessons.count()
    

class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ['id', 'title', 'video_url', 'resource', 'order']


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = CourseLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'duration', 'price',
            'instructor_name', 'instructor_photo', 'thumbnail',
            'what_you_learn', 'who_is_for', 'access_code',
            'created_at', 'lessons'
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']



class StrategyCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyCall
        fields = [
            'id', 'call_type', 'full_name', 'email', 'phone_number',
            'country', 'organization_name', 'stage', 'goal',
            'preferred_date', 'preferred_time', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class SpeakerInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakerInvitation
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'country',
            'organization_name',
            'event_structure',
            'message',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

