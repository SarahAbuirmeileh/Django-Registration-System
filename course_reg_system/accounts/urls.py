from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static 
from accounts import views

urlpatterns = [
    path('', views.get_home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/<str:student_name>/', views.home, name='home'),
    path('register/', views.register, name='register'),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)