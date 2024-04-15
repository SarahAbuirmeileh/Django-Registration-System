from django.urls import path
from courses import views

urlpatterns = [
    path('course/<int:course_id>/', views.course_details, name='course_details'),
]

