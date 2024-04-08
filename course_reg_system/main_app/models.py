from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.student_name

class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    instructor_name = models.CharField(max_length=100)
    schedule = models.ForeignKey('CourseSchedule', on_delete=models.CASCADE, null=True, blank=True)
    prerequisites = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    capacity = models.IntegerField()

    def __str__(self):
        return self.course_name

class CourseSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    days = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Schedule {self.schedule_id} ({self.days} {self.start_time}-{self.end_time})"

class StudentRegistration(models.Model):
    registration_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student {self.student.student_name} registered for {self.course.course_name}"
