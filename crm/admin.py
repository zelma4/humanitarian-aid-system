from django.contrib import admin
from .models import Recipient, LogisticsTrackingSystem, HelpRequest, Coordinator, Supplier, MonitoringAgency, HumanitarianAidSystem

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('recipientid', 'organizationName', 'address', 'phone_number', 'email')
    search_fields = ('organizationName',)

admin.site.register(LogisticsTrackingSystem)
admin.site.register(HelpRequest)
@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('coordinatorId', 'name', 'role', 'phone_number', 'email')
    search_fields = ('name', 'role')
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplierId', 'name', 'address', 'phone_number', 'email')
    search_fields = ('name',)
@admin.register(MonitoringAgency)
class MonitoringAgencyAdmin(admin.ModelAdmin):
    list_display = ('monitoryagencyId', 'name', 'address', 'phone_number', 'email')
    search_fields = ('name',)
admin.site.register(HumanitarianAidSystem)







