from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee, Attendance
from .forms import EmployeeForm, AttendanceForm

def hr_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('hr_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('hr_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('hr_register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_staff = True  # Mark as HR staff
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        login(request, user)  # Auto-login after registration
        return redirect('dashboard')

    return render(request, 'register.html')

def hr_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect logged-in users

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to HR dashboard
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def hr_logout(request):
    logout(request)
    return redirect('hr_login')

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee has been added successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employee_form.html', {'form': form})

@login_required
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee has been updated successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})

@login_required
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.success(request, 'Employee has been deleted successfully!')
    return redirect('employee_list')

@login_required
def attendance_list(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'attendance_list.html', {'attendance_records': attendance_records})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance has been marked successfully!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance_form.html', {'form': form})

# Only allow users in the "HR" group
def is_hr(user):
    return user.groups.filter(name="HR").exists()

@login_required
@user_passes_test(is_hr)
def hr_settings(request):
    return render(request, 'hr_settings.html')