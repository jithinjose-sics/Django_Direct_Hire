from django.urls import path
from .views import *
app_name='accounts'

urlpatterns = [
    path('', Home, name='home'),
    path('empregister/', EmployeeRegister2, name='reg_emp'),
    path('empregister2/', EmployeeRegister2, name='reg_emp2'),
    path('empregister3/', EmployeeRegister3, name='reg_emp3'),
    path('customerregister/', CustomerRegister, name='reg_cust'),
    path('customerregister2/', CustomerRegister2, name='reg_cust2'),
    path('login/', LoginView2, name='login'),
    path('login2/', LoginView2, name='login2'),
    path('customerpage/', CustomerPage, name='customerpage'),
    path('customerorders/', CustomerOrders, name='customer_orders'),
    path('closeorder/<str:pk>/', CloseOrder, name='close_order'),
    path('employeepage/', EmployeePage, name='employeepage'),
    path('approveorder/<str:pk>/', ApproveOrders, name='approve_order'),
    path('employee/<int:employee_id>/', EmployeeDetails, name='employeedetails'),
    path('booked/', BookedList, name='booked'),
    path('notification/', NotificationList, name='notification'),
    path('logout/', logout_view, name='logout'),
    path('job/<int:job_id>/', EmployeeList2, name='emp_list'),
    path('confirmedlist/',ConfirmedList, name="confirmed"),
    path('aboutus/', AboutUs, name='about_us'),
]