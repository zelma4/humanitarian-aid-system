# crm/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group

import csv
import io
import base64
import matplotlib.pyplot as plt

# Імпортуємо ваші моделі й форми
from .models import (
    Recipient,
    HelpRequest,
    Coordinator,
    Supplier,
    MonitoringAgency,
    # Якщо у вас є ще якісь моделі, додайте їх тут[thinking]


)

from .forms import (
    # Якщо хочете свою форму реєстрації, поставте замість UserCreationForm
    UserRegisterForm,
    RecipientForm,
    HelpRequestForm,
    CoordinatorForm,
    SupplierForm,
    MonitoringAgencyForm,
    RecipientSearchForm,
    HelpRequestSearchForm,
    CoordinatorSearchForm,
    SupplierSearchForm,
    MonitoringAgencySearchForm
)

# --------------------------------------------------
# 1. ГОЛОВНА СТОРІНКА + Авторизація
# --------------------------------------------------

def home(request):
    """
    Renders the homepage.
    """
    return render(request, 'crm/home.html')

def register_view(request):
    """
    Реєстрація нового користувача з вибором ролі.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            # Юзер вже створений, але ще не збережений у БД повністю
            
            role = form.cleaned_data['role']  # Отримуємо роль із форми
            user.save()                       # Зберігаємо користувача
            
            # Додаємо користувача до відповідної групи
            group = Group.objects.get(name=role)  # Переконайтесь, що група існує!
            user.groups.add(group)
            
            messages.success(request, f"Registration successful as {role}. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserRegisterForm()
    return render(request, 'crm/register.html', {'form': form})

def login_view(request):
    """
    Логін користувача через Django AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # авторизація
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('home')  
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'crm/login.html', {'form': form})

def logout_view(request):
    """
    Логаут (вихід) і редірект на сторінку логіну.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# --------------------------------------------------
# 2. Декоратори / Перевірка груп
# --------------------------------------------------

def user_is_coordinator_or_supplier(user):
    """
    Перевіряє, чи користувач у групі Coordinator або Supplier.
    """
    return user.groups.filter(name__in=['Coordinator', 'Supplier']).exists()

def user_is_manager(user):
    """
    Перевіряє, чи користувач у групі Manager.
    """
    return user.groups.filter(name='Manager').exists()


# --------------------------------------------------
# 3. Додавання об’єктів (ADD-views)
# --------------------------------------------------

@login_required
def add_recipient(request):
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipient added successfully.')
            return redirect('home')
        else:
            messages.error(request, "Error adding Recipient. Please check the form.")
    else:
        form = RecipientForm()
    return render(request, 'crm/add_recipient.html', {'form': form})


@login_required
def add_help_request(request):
    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            help_request = form.save(commit=False)
            # можна ще щось додати (автор, дати і т.д.)
            help_request.save()
            messages.success(request, 'Help request added successfully.')
            return redirect('home')
        else:
            messages.error(request, "Error creating Help Request. Please check the form.")
    else:
        form = HelpRequestForm()
    return render(request, 'crm/add_help_request.html', {'form': form})


@login_required
def add_coordinator(request):
    if request.method == 'POST':
        form = CoordinatorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coordinator added successfully.')
            return redirect('home')
        else:
            messages.error(request, "Error adding Coordinator. Please check the form.")
    else:
        form = CoordinatorForm()
    return render(request, 'crm/add_coordinator.html', {'form': form})


@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully.')
            return redirect('home')
        else:
            messages.error(request, "Error adding Supplier. Please check the form.")
    else:
        form = SupplierForm()
    return render(request, 'crm/add_supplier.html', {'form': form})


@login_required
def add_monitoring_agency(request):
    if request.method == 'POST':
        form = MonitoringAgencyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Monitoring agency added successfully.')
            return redirect('home')
        else:
            messages.error(request, "Error adding Monitoring Agency. Please check the form.")
    else:
        form = MonitoringAgencyForm()
    return render(request, 'crm/add_monitoring_agency.html', {'form': form})


# --------------------------------------------------
# 4. Списки (List-views) з пошуком (де потрібно)
# --------------------------------------------------

@login_required
def list_recipients(request):
    """
    Список отримувачів з пошуком (organizationName).
    """
    form = RecipientSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        recipients = Recipient.objects.filter(organizationName__icontains=query)
    else:
        recipients = Recipient.objects.all()
    return render(request, 'crm/list_recipients.html', {
        'recipients': recipients,
        'form': form
    })


@login_required
def list_help_requests(request):
    """
    Список HelpRequests:
      - Якщо користувач Manager, то показуємо лише,
        де coordinator_approved=True, supplier_approved=True і не відхилені.
      - Інакше показуємо всі (Coordinator, Supplier, інші).
    """
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name

    if user_group == 'Manager':
        help_requests = HelpRequest.objects.filter(
            coordinator_approved=True,
            supplier_approved=True,
            rejected=False
        )
    else:
        help_requests = HelpRequest.objects.all()

    return render(request, 'crm/list_help_requests.html', {
        'help_requests': help_requests
    })


@login_required
def list_coordinators(request):
    """
    Список координаторів з пошуком (name).
    """
    form = CoordinatorSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        coordinators = Coordinator.objects.filter(name__icontains=query)
    else:
        coordinators = Coordinator.objects.all()
    return render(request, 'crm/list_coordinators.html', {
        'coordinators': coordinators,
        'form': form
    })


@login_required
def list_suppliers(request):
    """
    Список постачальників з пошуком (name).
    """
    form = SupplierSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        suppliers = Supplier.objects.filter(name__icontains=query)
    else:
        suppliers = Supplier.objects.all()
    return render(request, 'crm/list_suppliers.html', {
        'suppliers': suppliers,
        'form': form
    })


@login_required
def list_monitoring_agencies(request):
    """
    Список моніторингових агенцій з пошуком (name).
    """
    form = MonitoringAgencySearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        agencies = MonitoringAgency.objects.filter(name__icontains=query)
    else:
        agencies = MonitoringAgency.objects.all()
    return render(request, 'crm/list_monitoring_agencies.html', {
        'monitoring_agencies': agencies,
        'form': form
    })


# --------------------------------------------------
# 5. Редагування / Видалення об’єктів
# --------------------------------------------------

@login_required
def edit_recipient(request, recipient_id):
    recipient = get_object_or_404(Recipient, pk=recipient_id)
    if request.method == 'POST':
        form = RecipientForm(request.POST, instance=recipient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipient updated successfully.')
            return redirect('list_recipients')
        else:
            messages.error(request, "Error updating Recipient. Please check the form.")
    else:
        form = RecipientForm(instance=recipient)
    return render(request, 'crm/edit_recipient.html', {'form': form})


@login_required
def delete_recipient(request, recipient_id):
    recipient = get_object_or_404(Recipient, pk=recipient_id)
    if request.method == 'POST':
        recipient.delete()
        messages.success(request, 'Recipient deleted successfully.')
        return redirect('list_recipients')
    return render(request, 'crm/delete_recipient.html', {'recipient': recipient})


# --------------------------------------------------
# 6. Approve / Reject: Coordinator, Supplier, Manager
# --------------------------------------------------

"""
Замість 6 окремих функцій (coordinator_approve, supplier_approve і т.д.) 
ми використовуємо дві універсальні (approve_help_request, reject_help_request)
з перевіркою груп. Для менеджера — окремі функції manager_approve / manager_reject.
Якщо хочете відділити Coordinator / Supplier — можна зробити окремі функції.
"""

@login_required
@user_passes_test(user_is_coordinator_or_supplier)
def approve_help_request(request, request_id):
    """
    Coordinator або Supplier схвалює запит.
    Якщо обидва схвалили => status = True.
    """
    help_request = get_object_or_404(HelpRequest, pk=request_id)
    user_group = request.user.groups.first().name

    if user_group == 'Coordinator':
        help_request.coordinator_approved = True
    elif user_group == 'Supplier':
        help_request.supplier_approved = True

    # Якщо Coordinator і Supplier схвалили, встановлюємо status = True
    if help_request.coordinator_approved and help_request.supplier_approved:
        help_request.status = True

    help_request.rejected = False  # Якщо було відхилено раніше
    help_request.save()
    # Якщо у вашій моделі є метод update_status(), викличте його:
    if hasattr(help_request, 'update_status'):
        help_request.update_status()

    messages.success(request, 'Help request approved successfully.')
    return redirect('list_help_requests')


@login_required
@user_passes_test(user_is_coordinator_or_supplier)
def reject_help_request(request, request_id):
    """
    Coordinator або Supplier відхиляє запит.
    """
    help_request = get_object_or_404(HelpRequest, pk=request_id)
    help_request.rejected = True
    # При відхиленні можна обнулити поля, наприклад:
    user_group = request.user.groups.first().name
    if user_group == 'Coordinator':
        help_request.coordinator_approved = False
    elif user_group == 'Supplier':
        help_request.supplier_approved = False

    help_request.save()
    if hasattr(help_request, 'update_status'):
        help_request.update_status()

    messages.success(request, 'Help request rejected successfully.')
    return redirect('list_help_requests')


@login_required
@user_passes_test(user_is_manager)
def manager_approve_help_request(request, request_id):
    """
    Менеджер схвалює запит.
    """
    help_request = get_object_or_404(HelpRequest, pk=request_id)
    help_request.manager_approved = True
    help_request.rejected = False
    help_request.save()
    if hasattr(help_request, 'update_status'):
        help_request.update_status()

    messages.success(request, 'Help request approved by manager successfully.')
    return redirect('list_help_requests')


@login_required
@user_passes_test(user_is_manager)
def manager_reject_help_request(request, request_id):
    """
    Менеджер відхиляє запит.
    """
    help_request = get_object_or_404(HelpRequest, pk=request_id)
    help_request.rejected = True
    help_request.manager_approved = False
    help_request.save()
    if hasattr(help_request, 'update_status'):
        help_request.update_status()

    messages.success(request, 'Help request rejected by manager successfully.')
    return redirect('list_help_requests')


# --------------------------------------------------
# 7. Звіти та Статистика
# --------------------------------------------------

@login_required
@user_passes_test(lambda u: u.is_staff)
def generate_report(request):
    """
    Генерує CSV-звіт про HelpRequests і їхніх Recipients.
    Доступ лише для staff (is_staff).
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Recipient ID', 'Organization Name', 'Contact Info',
                     'Request ID', 'Request Details', 'Request Status'])

    help_requests = HelpRequest.objects.select_related('recipient').all()
    for hr in help_requests:
        recipient = hr.recipient
        writer.writerow([
            recipient.recipientid,
            recipient.organizationName,
            recipient.contactinfo,
            hr.requestId,
            hr.requestDetails,
            hr.status
        ])

    return response


@staff_member_required
def statistics(request):
    """
    Приклад побудови графіка (барчарт) за пріоритетом HelpRequests.
    Доступ лише для staff.
    """
    priorities = ['Low', 'Medium', 'High']
    counts = [HelpRequest.objects.filter(priority=pr).count() for pr in priorities]

    plt.figure(figsize=(10, 5))
    plt.bar(priorities, counts, color=['green', 'orange', 'red'])
    plt.xlabel('Priority')
    plt.ylabel('Number of Requests')
    plt.title('Number of Help Requests by Priority')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'crm/statistics.html', {'image_base64': image_base64})