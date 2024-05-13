from django.db import models
from schedules.models import CourseSchedule

class Course(models.Model):
    course_code = models.CharField(primary_key=True, max_length=10)
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    instructor_name = models.CharField(max_length=100)
    schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, null=True, blank=True)
    prerequisites = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    capacity = models.IntegerField()

    def __str__(self):
        return self.course_name
