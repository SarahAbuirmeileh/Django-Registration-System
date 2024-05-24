from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import Student
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from accounts.models import UserImage

    

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            student = Student.objects.get(email=email)
            user = User.objects.get(email=email)
            std_name = None
            if student is not None:
                std_name = student.student_name
            std = authenticate(username=std_name, password=password)
            if std is not None:
                request.session['student_id'] = student.student_id
                try:
                    user_image = UserImage.objects.get(user=user)
                    request.session['profile_image_url'] = user_image.image.url if user_image.image else None
                except UserImage.DoesNotExist:
                    request.session['profile_image_url'] = None
                return redirect('home', student_name=student.student_name)  
            else:
                messages.error(request, 'Invalid email or password')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')


def logout(request):
    if 'student_id' in request.session:
        del request.session['student_id']
        del request.session['profile_image_url']
    auth.logout(request)
    return redirect('login') 


def home(request, student_name):
    return render(request, 'home.html', {'student_name': student_name})

def get_home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')
        profile_image = request.FILES.get('profile_image')

        try:
            # Validate email uniqueness
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered')
                return redirect('register')
            
            if Student.objects.filter(student_id=student_id).exists():
                messages.error(request, 'Student ID is already in use')
                return redirect('register')
            
            # Validate password complexity
            try:
                validate_password(password)
            except ValidationError as error:
                messages.error(request, ' '.join(error.messages))
                return redirect('register')
            
            # Save user
            user = User.objects.create_user(username=student_name, email=email, password=password)
            student = Student.objects.create(student_name=student_name, email=email, student_id=student_id)

            # Save profile image
            if profile_image:
                # user_image = UserImage.objects.create(user=user, image=profile_image, caption="User Profile")
                user_image = UserImage(image=profile_image, user=user, caption="Profile Image")
                user_image.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'An error occurred during registration.')
            return redirect('register')
    else:
        return render(request, 'register.html')
