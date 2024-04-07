from django.contrib import admin
from .models import Student, Course, CourseSchedule, StudentRegistration

# Register models
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CourseSchedule)
admin.site.register(StudentRegistration)

