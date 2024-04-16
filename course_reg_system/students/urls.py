from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.get_all_students, name='get_all_students'),
    path('student/<int:id>/', views.student_details, name='get_student_details'),
    path('student/<int:id>/', views.student_details, name='edit_student'),
    path('student/<int:id>/', views.student_details, name='delete_student'),
    path('student/<int:student_id>/course/<int:course_id>/', views.add_course_to_schedule,name='add_course_to_schedule'),
    # path('student/<int:student_id>/schedule/', views.get_student_schedule, name='get_student_schedule'),
    # path('student/<int:student_id>/notifications/', views.get_student_notifications, name='get_student_notifications'),
]
