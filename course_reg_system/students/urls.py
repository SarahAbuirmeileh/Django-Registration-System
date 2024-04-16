from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.get_all_students, name='get_all_students'),
    path('student/<int:id>/', views.student_details, name='get_student_details'),
    path('student/<int:id>/', views.student_details, name='edit_student'),
    path('student/<int:id>/', views.student_details, name='delete_student'),
]
