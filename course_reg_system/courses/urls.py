from django.urls import path
from courses import views

urlpatterns = [
    path('course/search/', views.search_course, name='search_course'),
    path('course/', views.get_all_courses, name='get_all_courses'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
]

