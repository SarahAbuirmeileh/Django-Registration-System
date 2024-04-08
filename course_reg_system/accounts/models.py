from django.db import models

class CourseSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    days = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Schedule {self.schedule_id} ({self.days} {self.start_time}-{self.end_time})"
