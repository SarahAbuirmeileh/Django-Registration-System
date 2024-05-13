from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CourseSchedule
from .serializers import CourseScheduleSerializer
from students.models import StudentRegistration
from django.shortcuts import render, redirect


@api_view(['GET', 'POST'])
def schedule_creation_retrieval(request):
    if request.method == 'POST':
        serializer = CourseScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        current_student_id = request.session.get('student_id')
        if current_student_id is not None:
            try:
                # Fetch all courses registered by the current student
                registered_courses = StudentRegistration.objects.filter(student=current_student_id).values_list('course', flat=True)

                # Fetch all schedules associated with the registered courses
                schedules = CourseSchedule.objects.filter(course__id__in=registered_courses)
                serializer = CourseScheduleSerializer(schedules, many=True)
                return render(request, 'courses_schedules.html', {'schedules': serializer.data})
            except StudentRegistration.DoesNotExist:
                # Handle the case where the student does not exist
                return render(request, 'courses_schedules.html', {'schedules': []})
        else:
            return redirect("login")
            # Handle the case where the student ID is not provided
            # schedules = CourseSchedule.objects.all()
            # serializer = CourseScheduleSerializer(schedules, many=True)
            
            # return render(request, 'courses_schedules.html', {'schedules': serializer.data})


@api_view(['PATCH', 'DELETE', 'GET'])
def schedule_update_delete_get(request, pk):
    try:
        schedule = CourseSchedule.objects.get(pk=pk)
    except CourseSchedule.DoesNotExist:
        return Response({"message": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = CourseScheduleSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if schedule.delete():
            return JsonResponse({"message": "Schedule deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message": "Failed to delete schedule"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        if schedule:
            try:
                serializer = CourseScheduleSerializer(schedule)
                return Response(serializer.data)
            except CourseSchedule.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            schedules = CourseSchedule.objects.all()
            serializer = CourseScheduleSerializer(schedules, many=True)
            return Response(serializer.data)