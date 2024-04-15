from django.http import HttpResponse
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

