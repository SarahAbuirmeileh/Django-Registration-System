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


class CourseDetailSerializer(serializers.ModelSerializer):
    schedule = CourseScheduleSerializer()
    prerequisites = serializers.SerializerMethodField()
    available_spots = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'description', 'instructor_name', 'schedule', 'prerequisites', 'capacity', 'available_spots']

    def get_prerequisites(self, obj):
        if obj.prerequisites:
            return f"{obj.prerequisites.course_name} {obj.prerequisites.course_code}"
        return None

    def get_available_spots(self, obj):
        if obj.capacity and obj.students.exists():
            available_spots = obj.capacity - obj.students.count()
            return f"{available_spots}/{obj.capacity}"
        return f"{obj.capacity}/{obj.capacity}"

class CourseSerializer(serializers.ModelSerializer):
    available_spots = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'description', 'instructor_name', 'schedule', 'prerequisites', 'capacity', 'available_spots']

    def get_available_spots(self, obj):
        if obj.capacity and obj.students.exists():
            return obj.capacity - obj.students.count()
        return obj.capacity