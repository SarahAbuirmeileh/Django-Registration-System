from rest_framework import serializers
from .models import Student, Deadline


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class DeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadline
        fields = ['id', 'name', 'description', 'due_date']
