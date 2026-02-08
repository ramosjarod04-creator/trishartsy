from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['fullname', 'email', 'contact', 'date', 'artstyle', 'art_image', 'payment_reference']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }