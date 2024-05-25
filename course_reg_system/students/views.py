from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student, StudentRegistration, Deadline
from .serializers import StudentSerializer, DeadlineSerializer
from courses.serializers import CourseSerializer
from courses.models import Course
from django.db.models import Q


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
from django.http import HttpResponse

@api_view(['PUT'])
def add_course_to_schedule(request, course_code):
    try:
        student_id = request.session.get('student_id')
        if not student_id:
            return Response( "Student not authenticated", status=status.HTTP_401_UNAUTHORIZED)

        student = Student.objects.get(student_id=student_id)
        course = Course.objects.get(course_code=course_code)
    except (Student.DoesNotExist, Course.DoesNotExist):
        return Response("Student or course not found", status=status.HTTP_404_NOT_FOUND)

    # Check if the student is already registered for the course
    if student.courses.filter(course_code=course_code).exists():
        return Response("Student is already registered for this course", status=status.HTTP_400_BAD_REQUEST)

    # Check if the student has completed all prerequisites for the course
    if course.prerequisites:
        if not StudentRegistration.objects.filter(student=student, course=course.prerequisites).exists():
            return Response("Student has not completed prerequisites for this course", status=status.HTTP_400_BAD_REQUEST)

    # Check if there is available capacity for the course
    if StudentRegistration.objects.filter(course=course).count() >= course.capacity:
        return Response("Course capacity is full", status=status.HTTP_400_BAD_REQUEST)

    registration = StudentRegistration.objects.create(student=student, course=course)
    registration.save()

    return Response("Course added to schedule successfully", status=status.HTTP_200_OK)


@api_view(['GET'])
def get_student_schedule(request):
    try:
        student_id=request.session['student_id']
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    schedule = student.courses.all()
    serializer = CourseSerializer(schedule, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_deadlines(request):
    deadlines = Deadline.objects.all()  # Retrieve all deadlines
    serializer = DeadlineSerializer(deadlines, many=True)
    return render(request, 'deadlines.html', {'deadlines': serializer.data})