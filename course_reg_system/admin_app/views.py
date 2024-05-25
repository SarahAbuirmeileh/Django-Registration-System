from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from schedules.serializers import CourseScheduleSerializer
from courses.serializers import CourseDetailSerializer
from courses.models import Course
from students.models import StudentRegistration
from .serializers import CourseSerializer
from students.serializers import DeadlineSerializer
from students.models import Student, Deadline
from schedules.models import CourseSchedule
from rest_framework.response import Response
from django.http import HttpResponse



@api_view(['DELETE', 'POST', 'GET'])
def delete_edit_course(request, course_id):

    if request.user.is_staff:  
    
        # ToDo: course_id or course_code
        course = get_object_or_404(Course, pk=course_id)
        # course = Course.objects.get(course_code = course_id)

        if request.method == 'DELETE':
            if course.delete():
                return Response({"message": "Course deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Failed to delete course"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'POST':
            course_fields = ['course_code', 'course_name', 'description', 'instructor_name', 'capacity']
            for field in course_fields:
                if field in request.POST and request.POST[field] != '':
                    setattr(course, field, request.POST[field])
            course.save() 
            
            return redirect('get_all_courses')

        elif request.method == 'GET':
            schedules = CourseSchedule.objects.all()
            courses = Course.objects.all()

            serializer = CourseDetailSerializer(courses, many=True)
            prerequisites = serializer.data
            serializer = CourseScheduleSerializer(schedules, many=True)
            schedules = serializer.data
        
            context = {
                'schedules': schedules,
                'prerequisites': prerequisites,
            }

            return render(request, 'course_edit.html', context)
    else:
        return redirect('home') 


@api_view(['GET'])
def generate_reports(request):
    if request.method == 'GET':
        try:
            # if request.user.is_staff:
                # Query all students registered for courses
            student_regs = StudentRegistration.objects.all()

            # Calculate total number of students registered for each course
            courses_enrollments = {}
            for reg in student_regs:
                try:
                    if reg.course_id in courses_enrollments:
                        courses_enrollments[reg.course_id] += 1
                    else:
                        courses_enrollments[reg.course_id] = 1
                except Exception as e:
                    print(f"Error processing registration {reg.registration_id}: {e}")
                        
            # Query course details
            courses = Course.objects.all()

            # Calculate course popularity
            courses_data = []
            for course in courses:
                if course.course_code in courses_enrollments:
                    popularity_score = courses_enrollments.get(course.course_code, 0)
                    instructor_name = course.instructor_name  
                    courses_data.append({'course_code': course.course_code, 'popularity_score': popularity_score, 'instructor_name': instructor_name})

            data = {
                'courses_data': courses_data,
            }
            return render(request, 'courses_reports.html', data)
            # else:
            #     # Return Forbidden response if user is not staff
            #     return Response({'message': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        except StudentRegistration.DoesNotExist:
            # Return response if no students are registered
            return render(request, 'courses_reports.html', {'message': 'No students registered for courses.'})
    else:
        # Return Method Not Allowed response for other request methods
        return Response({'message': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', 'GET'])
def create_course(request):
    if request.user.is_staff:
        if request.method == 'POST':
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return redirect('get_all_courses')
            return redirect('get_all_courses')
        
        elif request.method == 'GET':
            schedules = CourseSchedule.objects.all()
            courses = Course.objects.all()

            serializer = CourseDetailSerializer(courses, many=True)
            prerequisites = serializer.data
            serializer = CourseScheduleSerializer(schedules, many=True)
            schedules = serializer.data
        
            context = {
                'schedules': schedules,
                'prerequisites': prerequisites,
            }

            return render(request, 'course_create.html', context)
    else:
        return redirect('home') 


@api_view(['POST', 'GET'])
def create_deadline(request):
    if request.user.is_staff:
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
                    return redirect('get_deadlines')
                
        elif request.method == 'GET':
            return render(request, 'deadline_create.html')
    else:
        return redirect('home')


@api_view(['DELETE', 'POST', 'GET'])
def delete_edit_deadline(request, deadline_id):
    
    if request.user.is_staff:
        deadline = get_object_or_404(Deadline, pk=deadline_id)

        if request.method == 'DELETE':
            if deadline.delete():
                return Response({"message": "Deadline deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Failed to delete deadline"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'POST':
            deadline_fields = ['name', 'description', 'due_date']
            for field in deadline_fields:
                if field in request.POST and request.POST[field] != '':
                    setattr(deadline, field, request.POST[field])
            deadline.save() 
            
            return redirect('get_deadlines')
        
        elif request.method == 'GET':
            return render(request, 'deadline_edit.html')

    else:
        return redirect('home')

