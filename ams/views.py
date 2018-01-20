from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404

from .forms import UserForm, AssetForm
from .models import *


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'ams/login.html')
    else:
        employee = Employee.objects.filter(user=request.user)
        assets = Ownership.objects.filter(owner=employee)
        return render(request, 'ams/index.html', {'assets': assets})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'ams/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                employee = Employee.objects.filter(user=request.user)
                assets = Ownership.objects.filter(owner=employee)
                return render(request, 'ams/index.html', {'assets': assets})
            else:
                return render(request, 'ams/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'ams/login.html', {'error_message': 'Invalid login'})
    return render(request, 'ams/login.html')


def subordinates(request):
    if not request.user.is_authenticated():
        return render(request, 'ams/login.html')
    else:
        employee = Employee.objects.filter(user=request.user)
        all_subordinates = Employee.objects.filter(manager=employee)
        for sub in all_subordinates:
            booked = Ownership.objects.filter(owner=sub, status=Ownership.BOOKED)
            setattr(sub, 'booked', booked.count())
        return render(request, 'ams/subordinates.html', {'all_subordinates': all_subordinates})


def approval(request, employee_id):
    if not request.user.is_authenticated():
        return render(request, 'ams/login.html')
    else:
        employee = Employee.objects.filter(pk=employee_id)
        assets = Ownership.objects.filter(owner=employee)
        return render(request, 'ams/approval.html', {'assets': assets})


def approved(request, ownership_id):
    asset = get_object_or_404(Ownership, pk=ownership_id)
    all_subordinates = Employee
    try:
        asset.status = Ownership.APPROVED
        asset.save()
        employee = Employee.objects.filter(user=request.user)
        all_subordinates = Employee.objects.filter(manager=employee)
        for sub in all_subordinates:
            booked = Ownership.objects.filter(owner=sub, status=Ownership.BOOKED)
            setattr(sub, 'booked', booked.count())
    except (KeyError, Asset.DoesNotExist):
        return render(request, 'ams/subordinates.html', {'all_subordinates': all_subordinates})
    else:
        return render(request, 'ams/subordinates.html', {'all_subordinates': all_subordinates})


def employees(request):
    if not request.user.is_authenticated():
        return render(request, 'ams/login.html')
    else:
        all_employees = Employee.objects.all()
        return render(request, 'ams/employees.html', {'all_employees': all_employees})


def get_subordinates(emp):
    if Employee.objects.filter(manager=emp).count() > 0:
        emp_name = [emp.employee_name]
        all_subs = Employee.objects.filter(manager=emp)
        for sub in all_subs:
            emp_name.append(get_subordinates(sub))
        return emp_name
    else:
        return emp.employee_name


def deep_len(lst):
    return sum(deep_len(el) if isinstance(el, list) else 1 for el in lst)


def employee_detail(request, employee_id):
    if not request.user.is_authenticated():
        return render(request, 'ams/login.html')
    else:
        employee = Employee.objects.get(pk=employee_id)
        all_subordinates = get_subordinates(employee)
        if isinstance(all_subordinates, str):
                all_subordinates = [all_subordinates]
        return render(request, 'ams/employee_detail.html', {'all_subordinates': all_subordinates})


def employee_report(request):
    if not request.user.is_authenticated():
        return render(request, 'ams/login.html')
    else:
        all_employees = Employee.objects.all()
        for employee in all_employees:
            all_subordinates = get_subordinates(employee)
            if isinstance(all_subordinates, str):
                all_subordinates = [all_subordinates]
            setattr(employee, 'subordinates', deep_len(all_subordinates)-1)
        return render(request, 'ams/employee_report.html', {'all_employees': all_employees})


def asset_report(request):
    if not request.user.is_authenticated():
        return render(request, 'ams/login.html')
    else:
        all_departments = Department.objects.all()
        for dept in all_departments:
            employees_dept = Employee.objects.filter(department=dept)
            setattr(dept, 'employees', employees_dept.count())
            asset_count = 0
            for emp in employees_dept:
                asset_count += Ownership.objects.filter(owner=emp, status="Approved").count()
            setattr(dept, 'assets', asset_count)
        return render(request, 'ams/asset_report.html', {'all_departments': all_departments})


def request_asset(request):
    if not request.user.is_authenticated():
        return render(request, 'ams/login.html')
    else:
        form = AssetForm(request.POST or None)
        if form.is_valid():
            employee = Employee.objects.get(user=request.user)
            asset = form.save(commit=False)
            asset.owner = employee
            if employee.manager is not None:
                asset.status = Ownership.BOOKED
            else:
                asset.status = Ownership.APPROVED
            asset.save()
            assets = Ownership.objects.filter(owner=employee)
            return render(request, 'ams/index.html', {'assets': assets})
        context = {
            "form": form,
        }
        return render(request, 'ams/request_asset.html', context)
