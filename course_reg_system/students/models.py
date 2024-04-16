from django.db import models
from courses.models import Course

class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=20)
    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, through='StudentRegistration', related_name='students')

    def __str__(self):
        return self.student_name

class StudentRegistration(models.Model):
    registration_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student {self.student.student_name} registered for {self.course.course_name}"
