from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CourseSchedule
from .serializers import CourseScheduleSerializer


@api_view(['GET', 'POST'])
def schedule_creation_retrieval(request):
    if request.method == 'POST':
        serializer = CourseScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        schedule_id = request.query_params.get('id')
        if schedule_id:
            try:
                schedule = CourseSchedule.objects.get(pk=schedule_id)
                serializer = CourseScheduleSerializer(schedule)
                return Response(serializer.data)
            except CourseSchedule.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            schedules = CourseSchedule.objects.all()
            serializer = CourseScheduleSerializer(schedules, many=True)
            return Response(serializer.data)


@api_view(['PATCH', 'DELETE'])
def schedule_update_delete(request, pk):
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