from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from students.models import Student
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            student = Student.objects.get(email=email)
            if check_password(password, student.password):
                # Authentication successful, set session variables
                request.session['student_id'] = student.student_id
                # request.session.modified = True
                return redirect('home', student_name=student.student_name)  
            else:
                messages.error(request, 'Invalid email or password')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')


def logout(request):
    if 'student_id' in request.session:
        del request.session['student_id']
    return redirect('login')  # Redirect to login page after logout


def home(request, student_name):
    return render(request, 'home.html', {'student_name': student_name})

def get_home(request):
    return render(request, 'home.html')

# I tried to use django forms
# from django.contrib.auth.forms import UserCreationForm
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("You have been registered successfully")
#     else:
#         form = UserCreationForm()
#         return render(request, 'register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')  # Added line to get student ID

        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID is already in use')
            return redirect('register')

        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered')
            return redirect('register')

        try:
            # Password must contain at least 8 characters, shouldn't be too common or entirely numeric.
            validate_password(password)
        except ValidationError as error:
            messages.error(request, ' '.join(error.messages))
            return redirect('register')

        hashed_password = make_password(password)

        try:
            student = Student.objects.create(student_name=student_name, email=email, password=hashed_password,student_id=student_id)
        except Exception:
            messages.error(request, 'An error occurred during registration. Please try again later.')
            return redirect('register')

        messages.success(request, 'Registration has been completed successfully! Please login.')
        return redirect('login')

    return render(request, 'register.html')

