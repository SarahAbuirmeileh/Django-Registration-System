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
        fields = ['id', 'course_code', 'course_name', 'description', 'instructor_name', 'schedule', 'prerequisites', 'capacity']

    def get_prerequisites(self, obj):
        if obj.prerequisites:
            return {
                'prerequisite_course_code': obj.prerequisites.course_code,
                'prerequisite_course_name': obj.prerequisites.course_name,
            }
        return None


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'