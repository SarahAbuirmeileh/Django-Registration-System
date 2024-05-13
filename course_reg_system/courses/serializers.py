from rest_framework import serializers
from .models import Course
from schedules.models import CourseSchedule


class CourseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSchedule
        fields = ['schedule_id', 'days', 'start_time', 'end_time', 'room_number']


class CourseDetailSerializer(serializers.ModelSerializer):
    schedule = CourseScheduleSerializer()
    prerequisites = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'description', 'instructor_name', 'schedule', 'prerequisites', 'capacity']

    def get_prerequisites(self, obj):
        if obj.prerequisites:
            return {
                obj.prerequisites.course_name + ' ' + obj.prerequisites.course_code
            }
        return None


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'