from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from courses.models import Course
from students.models import StudentRegistration

@api_view(['DELETE'])
def delete_course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if course.delete():
            return JsonResponse({"message": "Course deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message": "Failed to delete course"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
