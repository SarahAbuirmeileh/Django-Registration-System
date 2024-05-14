from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Course
from .serializers import CourseDetailSerializer
from rest_framework.response import Response


@api_view(['GET'])
def course_details(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseDetailSerializer(course)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_courses(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseDetailSerializer(courses, many=True)
        return render(request, 'courses.html', {'courses': serializer.data})
        

@api_view(['GET'])
def search_course(request):

    # the user can search by more than one parameter
    # Example: /course/search/?course_name=World%20History&course_code=HIST101

    query_course_code = request.GET.get('course_code')
    query_course_name = request.GET.get('course_name')
    query_instructor_name = request.GET.get('instructor_name')

    courses = Course.objects.all()

    if query_course_code:
        courses = courses.filter(course_code__icontains=query_course_code)

    if query_course_name:
        courses = courses.filter(course_name__icontains=query_course_name)

    if query_instructor_name:
        courses = courses.filter(instructor_name__icontains=query_instructor_name)

    serializer = CourseDetailSerializer(courses, many=True)
    return render(request, 'courses.html', {'courses': serializer.data})