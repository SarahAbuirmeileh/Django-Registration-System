from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student, StudentRegistration, Deadline
from .serializers import StudentSerializer, DeadlineSerializer
from courses.serializers import CourseSerializer


@api_view(['GET'])
def get_all_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH', 'DELETE'])
def student_details(request, id):
    try:
        student = Student.objects.get(student_id=id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# views.py

@api_view(['PUT'])
def add_course_to_schedule(request, student_id, course_id):
    try:
        student = Student.objects.get(student_id=student_id)
        course = Course.objects.get(id=course_id)
    except (Student.DoesNotExist, Course.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if the student is already registered for the course
    if student.courses.filter(id=course_id).exists():
        return Response({"error": "Student is already registered for this course"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new StudentRegistration instance to register the student for the course
    registration = StudentRegistration.objects.create(student=student, course=course)
    registration.save()

    return Response({"message": "Course added to schedule successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_student_schedule(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    schedule = student.courses.all()
    serializer = CourseSerializer(schedule, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def student_deadlines(request):
    deadlines = Deadline.objects.all()  # Retrieve all deadlines
    serializer = DeadlineSerializer(deadlines, many=True)
    return Response(serializer.data)