from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from crm.models import HelpRequest

def run():
    recipient_group, created = Group.objects.get_or_create(name='Recipient')
    coordinator_group, created = Group.objects.get_or_create(name='Coordinator')
    supplier_group, created = Group.objects.get_or_create(name='Supplier')
    manager_group, created = Group.objects.get_or_create(name='Manager')

    help_request_content_type = ContentType.objects.get_for_model(HelpRequest)
    approve_permission = Permission.objects.create(
        codename='can_approve_help_request',
        name='Can approve help request',
        content_type=help_request_content_type,
    )
    reject_permission = Permission.objects.create(
        codename='can_reject_help_request',
        name='Can reject help request',
        content_type=help_request_content_type,
    )

    coordinator_group.permissions.add(approve_permission, reject_permission)
    supplier_group.permissions.add(approve_permission, reject_permission)
    manager_group.permissions.add(approve_permission, reject_permission)