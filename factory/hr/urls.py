from django.urls import path
from .views import hr_register,hr_login,dashboard,hr_logout

from .views import (
    employee_list, add_employee, update_employee, delete_employee,
    attendance_list, mark_attendance,hr_settings
)
from . import views

urlpatterns = [
    
    path('register/', hr_register, name='hr_register'),
    path('', hr_login, name='hr_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', hr_logout, name='hr_logout'),
    path('settings/', views.hr_settings, name='hr_settings'),
    path('employees/', employee_list, name='employee_list'),
    path('employees/add/', add_employee, name='add_employee'),
    path('employees/update/<int:pk>/', update_employee, name='update_employee'),
    path('employees/delete/<int:pk>/', delete_employee, name='delete_employee'),
    path('attendance/', attendance_list, name='attendance_list'),
    path('attendance/mark/', mark_attendance, name='mark_attendance'),
    
]