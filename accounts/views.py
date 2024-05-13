from django import contrib
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from .models import *
from .forms import *
from .filters import *
from django.utils import timezone
from datetime import date, datetime, time
import pytz

# Create your views here.

def Home(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if user_type == 1:
            job_list = JobList.objects.all()
            context = {'job_list': job_list}
            # print("----------------------Home-----------{}".format(request.user.user_type))
            return redirect('/customerpage')
        elif user_type == 2:
            return redirect('/employeepage')
        else:
            return redirect('/admin')
    else:
        job_list = JobList.objects.all()
        context = {'job_list': job_list}
        return render(request, "base.html", context)


def EmployeeList2(request,job_id):
    job_name = None
    list_emp = None
    list_emp = JobList.objects.get(id=job_id).employee_set.all().order_by('-emp_rating')
    job_name = JobList.objects.get(id=job_id)
    print('Job : {}'.format(job_name))
    myfilter = EmployeeFilter(request.GET, queryset=list_emp)
    list_emp = myfilter.qs
    for i in list_emp:
        print(i)
    job_list = JobList.objects.all()
    context = {
        'job_list': job_list,
        'job_id':job_id,
        'job_name':job_name,
        'emp_list':list_emp,
        'myfilter':myfilter
    }
    return render(request, 'employeelist.html', context)


def EmployeeRegister2(request):
    if request.method == 'POST':
        user = UserForm(data=request.POST)
        print("Form errors----------:",user.errors)
        if user.is_valid():
            print('---------------Valid User-------------------')
            password = request.POST['password1']
            user = user.save(commit=False)
            user.user_type = 2
            # user.set_password(password)
            user.save()
            userid = user.id
            username = user.username
            user = authenticate(request,username=username, password=password)
            print('---------------',user.username,'---------------------')
            if user is not None:
                login(request, user)
                return redirect('/empregister3')
        else:
            print('---------------inValid User-------------------')
            context = {'user': user}
            return render(request, 'register_employee2.html', context)
    else:
        user = UserForm(data=request.POST)
        user = UserForm()
        employee = EmployeeForm(data=request.POST)
        context = {'user': user}
    return render(request, 'register_employee2.html', context)


def EmployeeRegister3(request):
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, request.FILES)
        if employee_form.is_valid():
            employee = employee_form.save(commit=False)
            employee.user = request.user
            employee.save()
            return redirect('/')
    else:
        employee_form = EmployeeForm()
    return render(request, 'register_employee3.html', {'employee_form': employee_form})

def CustomerRegister2(request):
    print('Customer reg 2')
    if request.method=='POST':
        print('Inside cus reg 2')
        user = UserForm(data=request.POST)
        customer = CustomerForm(data=request.POST)
        if user.is_valid():
            print('cus 2 validated')
            password = request.POST['password1']
            # password = user.cleaned_data.get("password")
            user = user.save(commit=False)
            user.user_type = 1
            # user.set_password(password)
            user.save()
            userid = user.id
            username = user.username
            if customer.is_valid():
                user = NewUser.objects.get(id=userid)
                customer = customer.save(commit=False)
                customer.users = user
                customer.save()
                user = authenticate(request,username=username, password=password)
                if user is not None:
                    login(request, user)
                    # messages.info(request, "Successfully Registered")
                    return redirect('/')
            else:
                print('There is some issue in customer validation')
                print(customer.errors)
                user = UserForm()
                context = {'user':user,'customer': customer}
                return render(request,'register_customer2.html', context)
        else:
            print('Did not validate')
    else:
        print('Did not pass POST')
        user = UserForm(data=request.POST)
        customer = CustomerForm(data=request.POST)
    context = {'user':user,'customer': customer}
    return render(request,'register_customer2.html', context)


def LoginView2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # messages.info(request, "Successfully Logged In")
            print('-------------------------', user.user_type)
            return redirect('/')
        else:
            messages.info(request, "Login Failed : Invalid Credentials Provided")
            return redirect('/login2')
    else:
        return render(request, 'login2.html')


def CustomerPage(request):
    job_list = JobList.objects.all()
    context = {
        'job_list': job_list,
    }
    return render(request, 'customer_page.html', context)


def CustomerOrders(request):
    customer_orders = []
    approved_orders = []    
    # print(' customer orders : {}'.format(request.user.id))
    cus = Customer.objects.get(users__id=request.user.id)
    orders = cus.workdetails_set.all()
    total_orders_count = orders.count()
    unapproved_orders_count = orders.filter(job_status='Unapproved').count()
    closed_count = orders.filter(job_status='Closed').count()
    for i in orders:
        emp = i.employee_id
        # print(emp.name)
        # print(type(i.employee_id))
        customer_orders.append({'emp_name':emp.name, 'phone':emp.contact, 'location':i.location, 'date':i.date, 'status':i.job_status, 'job':emp.job, 'id':i.id})
        if i.job_status == 'Approved':
            approved_orders.append({'emp_name':emp.name, 'phone':emp.contact, 'location':i.location, 'date':i.date, 'status':i.job_status, 'job':emp.job, 'id':i.id})
    context = {
        'closed_count': closed_count,
        'unapproved_orders_count': unapproved_orders_count,
        'total_orders_count': total_orders_count,
        'customer_orders': customer_orders,
        'approved_orders':approved_orders
    }
    return render(request, 'customer_orders.html', context)


def CloseOrder(request, pk):
    date_check = False
    order = WorkDetails.objects.get(id=pk)

    # Check if the request is coming from an employee
    if request.user.user_type == 2:
        # If it's an employee, mark the order as closed and return to the employee page
        order.job_status = 'Closed'
        order.save()
        return redirect('/employeepage')

    if request.method == 'POST':
        # If it's a customer, check if the order date is valid for closure
        emp_rating = int(request.POST.get('emp_rating', 0))
        if emp_rating and 1 <= emp_rating <= 5:
            order.rating = emp_rating

        order.job_status = 'Closed'
        order.save()
        emp = order.employee_id
        emp_closed_orders = emp.workdetails_set.filter(job_status='Closed')
        closed_ord_count = len(emp_closed_orders)
        total_rating = sum(ordi.rating for ordi in emp_closed_orders if ordi.rating is not None)
        non_none_count = sum(1 for ordi in emp_closed_orders if ordi.rating is not None)
        avg_emp_rating = total_rating / non_none_count if non_none_count > 0 else 0
        emp.emp_rating = avg_emp_rating
        emp.save()
        return redirect('/customerorders')

    utc = pytz.UTC
    order_date = order.date
    current_date = utc.localize(datetime.now())
    if current_date < order_date:
        date_check = True

    context = {'date_check': date_check}
    return render(request, 'close_order.html', context)


def EmployeePage(request):
    print('Employee id :{}'.format(request.user.id))
    employee = Employee.objects.get(user__id=request.user.id)
    orders = employee.workdetails_set.all()
    total_orders_count = orders.count()
    unapproved_orders_count = orders.filter(job_status='Unapproved').count()
    closed_count = orders.filter(job_status='Closed').count()
    approved_orders = orders.filter(job_status='Approved')
    closed_orders = orders.filter(job_status='Closed')
    unapproved_orders = orders.filter(job_status='Unapproved')
    approved_cus_contacts = []
    closed_cus_contacts = []
    unapproved_orders_list = []
    for i in approved_orders:
        cus = Customer.objects.get(name=i.customer_id)
        approved_cus_contacts.append({'name':cus.name, 'phone':cus.contact, 'date':i.date, 'id': i.id})
    for i in closed_orders:
        cus = Customer.objects.get(name=i.customer_id)
        closed_cus_contacts.append({'name':cus.name, 'phone':cus.contact, 'date':i.date, 'id': i.id, 'rating':i.rating})
    for i in unapproved_orders:
        cus = Customer.objects.get(name=i.customer_id)
        unapproved_orders_list.append({'name':cus.name, 'phone':cus.contact, 'address':cus.address, 'date':i.date, 'location':i.location, 'id': i.id})
    print('This is approved customers : {}'.format(approved_cus_contacts))
    context = {
        'total_orders_count': total_orders_count,
        'unapproved_orders_count':unapproved_orders_count,
        'closed_count':closed_count,
        'approved_cus_contacts':approved_cus_contacts,
        'closed_cus_contacts':closed_cus_contacts,
        'unapproved_orders_list':unapproved_orders_list,
    }
    return render(request, 'employee_page.html', context)

def EmployeeDetails(request, employee_id):
    emp = Employee.objects.get(id=employee_id)
    customer = Customer.objects.get(users__id=request.user.id)
    print("Customer name: {}".format(customer.name))
    context = {'emp': emp, 'employee_id': employee_id}  # Include employee_id in the context
    
    if request.method == 'POST':
        time = request.POST.get('worktime')
        location = request.POST.get('location')
        current_datetime = timezone.now()
        
        tz = pytz.timezone('UTC') 
        work_datetime = tz.localize(datetime.strptime(time, '%Y-%m-%dT%H:%M'))
        
        if work_datetime < current_datetime:
            messages.error(request, "You cannot book for a past date and time.")
        else:
            print("This id customer id: {}".format(customer.id))
            work = WorkDetails(date=work_datetime, location=location, customer_id=customer, employee_id=emp, job_status='Unapproved')
            work.save()

            dateTime = work.date
            location = work.location
            employeeName = emp.name
            employeeEmail = emp.user.email
            customerName = customer.name
            customerPhone = customer.contact

            # messages.info(request, "Successfully Booked")
            return redirect('/')  # Redirect to the desired URL after successful booking
    
    # Render the same template with error messages if any validation fails
    context['messages'] = messages.get_messages(request)
    return render(request, 'employee_details.html', context)



def ApproveOrders(request, pk):
    order = WorkDetails.objects.get(id=pk)
    order.job_status = 'Approved'
    order.save()
    return redirect('/')


def AboutUs(request):
    return render(request, 'about_us.html')


def BookedList(request):
    return

def NotificationList(request):
    return


def logout_view(request):
    logout(request)
    return redirect('/')


def ConfirmedList(request):
    return




# ------------------------------------------------------------------OLD------------------------------------------------




def EmployeeRegister(request):
    if request.method == 'POST':
        user = UserForm(data=request.POST)
        employee = EmployeeForm(data=request.POST)
        if user.is_valid():
            password = user.cleaned_data.get("password")
            #id = user.cleaned_data.get("id")
            user = user.save(commit=False)
            user.user_type = 2
            user.set_password(password)
            user.save()
            userid = user.id
            if employee.is_valid():
                user = User.objects.get(id=userid)
                employee = employee.save(commit=False)
                employee.user = user
                employee.save()
                messages.info(request,"Successfully Registered")
                return redirect('/login')
    else:
        user = UserForm(data=request.POST)
        employee = EmployeeForm(data=request.POST)
        context = {
            'user':user,
            'employee': employee
        }
    return render(request, 'register_employee.html', context)


def CustomerRegister(request):
    print('Customer reg 1')
    if request.method=='POST':
        user = UserForm(data=request.POST)
        customer = CustomerForm(data=request.POST)
        if user.is_valid():
            password = user.cleaned_data.get("password")
            user = user.save(commit=False)
            user.user_type = 1
            user.set_password(password)
            user.save()
            userid = user.id
            if customer.is_valid():
                user = NewUser.objects.get(id=userid)
                customer = customer.save(commit=False)
                customer.users = user
                customer.save()
                messages.info(request, "Successfully Registered")
                return redirect('/login')
    else:
        user = UserForm(data=request.POST)
        customer = CustomerForm(data=request.POST)
    context = {'user':user,'customer': customer}
    return render(request,'register_customer.html', context)


def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #user=User.objects.filter(username=username,password=password).first()
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.info(request, "Successfully Logged In")
            return redirect('/')
        else:
            messages.info(request, "Login Failed : Invalid Credentials Provided")
            return redirect('/login')
    else:
        return render(request, 'login.html')


def EmployeeList(request,job_id):
    jobname = None
    list_emp = None
    list_emp = Employee.objects.filter(job=job_id).select_related('user')
    if list_emp:
        getJob = Employee.objects.filter(job=job_id).select_related('user').first()
        if getJob:
            jobname = str(getJob.job)
            jobname = jobname.capitalize()
        if request.method == 'GET':
            search_city = request.GET.get('q')
            print(search_city,"search")
            if search_city:
                if Employee.objects.filter(city=search_city).select_related('user').exists():
                    list_emp = Employee.objects.filter(city=search_city).select_related('user')
                else:
                    messages.info(request,"No results found")
    return render(request,"employeelist.html", {'list': list_emp, 'job':jobname})