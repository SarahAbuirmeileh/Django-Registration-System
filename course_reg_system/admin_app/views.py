from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from courses.models import Course
from students.models import StudentRegistration
from .serializers import CourseSerializer
from students.serializers import DeadlineSerializer
from students.models import Student, Deadline


@api_view(['DELETE', 'PATCH'])
def delete_edit_course(request, course_id):
    if request.method == 'DELETE':
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'DELETE':
            if course.delete():
                return JsonResponse({"message": "Course deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"message": "Failed to delete course"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PATCH':
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PATCH':
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def generate_reports(request):
    # Query all students registered for courses
    student_regs = StudentRegistration.objects.all()

    # Calculate total number of students registered for each course
    courses_enrollments = {}
    for reg in student_regs:
        course_code = reg.course.course_code
        if course_code in courses_enrollments:
            courses_enrollments[course_code] += 1
        else:
            courses_enrollments[course_code] = 1

    # Query course details
    courses = Course.objects.all()

    # Calculate course popularity based on some factors
    courses_popularity = {}
    for course in courses:
        # Calculating popularity based on number of enrollments
        popularity_score = courses_enrollments.get(course.course_code, 0)
        # We can add more factors here to determine course popularity
        courses_popularity[course.course_code] = popularity_score

        # Additional factors to consider
        # Factor 1: Course ratings
        # Assuming the Course model has a field for ratings
        # if course.ratings:
        #     popularity_score += course.ratings

        # Factor 2: Instructor reputation
        # Assuming the Course model has a field for instructor reputation
        # if course.instructor_reputation:
        #     popularity_score += course.instructor_reputation

        # Factor 3: Student feedback
        # Assuming we have a way to collect and analyze student feedback
        # We can calculate a score based on feedback and add it to popularity_score

    data = {
        'courses_enrollments': courses_enrollments,
        'courses_popularity': courses_popularity,
        # Add more data for other relevant reports
    }
    # return Response(data)
    return render(request, 'courses_reports.html', data)


@api_view(['POST'])
def create_course(request):
    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_deadline(request):
    if request.method == 'POST':
        serializer = DeadlineSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                deadline = serializer.save()

                students = Student.objects.all()
                for student in students:
                    send_mail(
                        f"New Deadline: {deadline.name}",
                        f"A new deadline '{deadline.name}' has been created. Make sure to check it.",
                        'sarahabuirmeileh@gmail.com',
                        [student.email],
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'PATCH'])
def delete_edit_deadline(request, deadline_id):
    deadline = get_object_or_404(Deadline, pk=deadline_id)

    if request.method == 'DELETE':
        deadline.delete()
        return JsonResponse({"message": "Deadline deleted successfully"}, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = DeadlineSerializer(deadline, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)