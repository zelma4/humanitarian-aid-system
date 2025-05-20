from django.db import models

PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

class Recipient(models.Model):
    recipientid = models.AutoField(primary_key=True)
    organizationName = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.organizationName

class HelpRequest(models.Model):
    requestId = models.AutoField(primary_key=True)
    requestDetails = models.TextField()
    coordinator_approved = models.BooleanField(default=False)
    supplier_approved = models.BooleanField(default=False)
    manager_approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    status = models.BooleanField(default=False)  # Кінцевий статус
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    recipient = models.ForeignKey('Recipient', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"HelpRequest #{self.requestId}"

    def update_status(self):
        """
        Логіка: якщо заявка не відхилена і coordinator, supplier і manager
        одночасно approved == True, тоді статус = True.
        В іншому випадку (або при rejected == True) — статус = False.
        """
        if self.rejected:
            self.status = False
        else:
            self.status = self.coordinator_approved and \
                          self.supplier_approved and \
                          self.manager_approved
        self.save()

ROLE_CHOICES = [
    ('Analyst', 'Analyst'),
    ('Manager', 'Manager'),
    ('Advisor', 'Advisor'),
    ('Liaison', 'Liaison'),
    ('Consultant', 'Consultant'),
    ('Logistics', 'Logistics'),
    ('Director', 'Director'),
    ('Coordinator', 'Coordinator'),
    ('Assistant', 'Assistant'),
    ('Field Officer', 'Field Officer'),
]

class Coordinator(models.Model):
    coordinatorId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)  # Оновлено
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

class Supplier(models.Model):
    supplierId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

class MonitoringAgency(models.Model):
    monitoryagencyId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

class LogisticsTrackingSystem(models.Model):
    trackingId = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False)
    wheredelivery = models.CharField(max_length=255)
    date_shipped = models.DateField(null=True, blank=True)
    date_delivered = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Tracking ID: {self.trackingId}"

class HumanitarianAidSystem(models.Model):
    humanitarianCoordinatorId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    assignedRegion = models.CharField(max_length=255)
    requestId = models.ForeignKey(HelpRequest, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='humanitarian_aid_systems')

    def __str__(self):
        return self.name