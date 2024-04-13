from django.urls import path
from . import views

urlpatterns = [
    path('schedules/', views.schedule_creation_retrieval, name='schedule-creation-retrieval'),
    path('schedules/<int:pk>/', views.schedule_update_delete, name='schedule-update-delete'),
]