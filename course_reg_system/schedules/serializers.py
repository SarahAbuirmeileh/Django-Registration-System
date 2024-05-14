from rest_framework import serializers
from .models import CourseSchedule
from courses.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'instructor_name']  

class CourseScheduleSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  

    class Meta:
        model = CourseSchedule
        fields = ['course', 'days', 'start_time', 'end_time', 'room_number']
