from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/<str:student_name>/', views.home, name='home'),
    path('register/', views.register, name='register'),
]
