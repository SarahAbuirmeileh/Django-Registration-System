from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from students.models import Student
from django.contrib.auth.hashers import make_password

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            student = Student.objects.get(email=email)
            if password == student.password:
                # Authentication successful, set session variables
                # This will be changed, we will use JWT later
                request.session['student_id'] = student.student_id
                return redirect('home', student_name=student.student_name)  # Redirect to home after login
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

        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered')
            return redirect('register')

        hashed_password = make_password(password)
        student = Student.objects.create(student_name=student_name, email=email, password=hashed_password)

        messages.success(request, 'Registration has been completed successfully! Please login.')
        return redirect('login')

    return render(request, 'register.html')
