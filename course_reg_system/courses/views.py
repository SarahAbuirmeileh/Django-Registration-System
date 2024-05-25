from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from students.models import Student, StudentRegistration
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
    if request.user.is_staff:
        courses = Course.objects.all()
    else:
        student_id = request.session.get('student_id')
        if student_id:
            try:
                student = Student.objects.get(student_id=student_id)
                student_courses = Course.objects.filter(prerequisites__isnull=True)  
                
                for course in student_courses:
                    prerequisites = course.prerequisites.all() if course.prerequisites else None
                    if prerequisites: 
                        for prerequisite in prerequisites:
                            if not StudentRegistration.objects.filter(student=student, course=prerequisite).exists():
                                student_courses = student_courses.exclude(pk=course.pk) 
                                break
                courses = student_courses
            except Student.DoesNotExist:
                courses = Course.objects.none()
        else:
            return redirect('login')
        
    serializer = CourseDetailSerializer(courses, many=True)
    return render(request, 'courses.html', {'courses': serializer.data})
     

@api_view(['GET'])
def search_course(request):
    query_course_name = request.GET.get('course_name', '')
    query_instructor_name = request.GET.get('instructor_name', '')
    query_course_code = request.GET.get('course_code', '')

    courses = Course.objects.all()

    if query_course_name:
        courses = courses.filter(course_name__icontains=query_course_name)

    if query_instructor_name:
        courses = courses.filter(instructor_name__icontains=query_instructor_name)

    if query_course_code:
        courses = courses.filter(course_code__icontains=query_course_code)


    serializer = CourseDetailSerializer(courses, many=True)
    return render(request, 'courses.html', {'courses': serializer.data})