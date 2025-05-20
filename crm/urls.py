from django.urls import path
from . import views

urlpatterns = [
    # Main page
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Add
    path('add_recipient/', views.add_recipient, name='add_recipient'),
    path('add_help_request/', views.add_help_request, name='add_help_request'),
    path('add_coordinator/', views.add_coordinator, name='add_coordinator'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('add_monitoring_agency/', views.add_monitoring_agency, name='add_monitoring_agency'),

    # List
    path('list_recipients/', views.list_recipients, name='list_recipients'),
    path('list_help_requests/', views.list_help_requests, name='list_help_requests'),
    path('list_coordinators/', views.list_coordinators, name='list_coordinators'),
    path('list_suppliers/', views.list_suppliers, name='list_suppliers'),
    path('list_monitoring_agencies/', views.list_monitoring_agencies, name='list_monitoring_agencies'),

    # Edit/delete
    path('edit_recipient/<int:recipient_id>/', views.edit_recipient, name='edit_recipient'),
    path('delete_recipient/<int:recipient_id>/', views.delete_recipient, name='delete_recipient'),

    # Approve / Reject
    path('approve_help_request/<int:request_id>/', views.approve_help_request, name='approve_help_request'),
    path('reject_help_request/<int:request_id>/', views.reject_help_request, name='reject_help_request'),

    # Manager Approve / Reject
    path('manager_approve_help_request/<int:request_id>/', views.manager_approve_help_request, name='manager_approve_help_request'),
    path('manager_reject_help_request/<int:request_id>/', views.manager_reject_help_request, name='manager_reject_help_request'),

    # Generate report/stats
    path('generate_report/', views.generate_report, name='generate_report'),
    path('statistics/', views.statistics, name='statistics'),
]