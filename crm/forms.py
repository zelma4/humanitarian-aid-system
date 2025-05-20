from django import forms
from .models import Recipient, HelpRequest, Coordinator, Supplier, MonitoringAgency, HumanitarianAidSystem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """
    Розширюємо стандартну UserCreationForm, додаючи поле 'role',
    яке потім використаємо, щоб додати користувача до групи.
    """
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Coordinator', 'Coordinator'),
        ('Supplier', 'Supplier'),
        ('Recipient', 'Recipient'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, help_text="Select your role.")

    class Meta:
        model = User
        fields = ('username', 'role', 'password1', 'password2')

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['organizationName', 'address', 'phone_number', 'email']

class HelpRequestForm(forms.ModelForm):
    PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ]
    
    class Meta:
        model = HelpRequest
        fields = ['recipient', 'requestDetails', 'priority']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CoordinatorForm(forms.ModelForm):
    class Meta:
        model = Coordinator
        fields = ['name', 'role', 'phone_number', 'email']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'address', 'phone_number', 'email']

class MonitoringAgencyForm(forms.ModelForm):
    class Meta:
        model = MonitoringAgency
        fields = ['name', 'address', 'phone_number', 'email']

class RecipientSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255, required=False)

class HelpRequestSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255, required=False)

class CoordinatorSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255, required=False)

class SupplierSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255, required=False)

class MonitoringAgencySearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255, required=False)