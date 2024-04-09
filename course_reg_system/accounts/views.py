from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from students.models import Student

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