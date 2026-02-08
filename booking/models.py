from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms


# ===============================
# CUSTOM USER MODEL (with roles)
# ===============================
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.role})"


# ===============================
# APPOINTMENT MODEL
# ===============================
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Denied', 'Denied'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=20)
    date = models.DateField()
    artstyle = models.CharField(max_length=100)

    # New fields for payment and uploaded art
    payment_reference = models.ImageField(
        upload_to='references/',
        null=True,
        blank=True,
        help_text="Upload GCash screenshot or reference"
    )
    art_image = models.ImageField(
        upload_to='art_uploads/',
        null=True,
        blank=True,
        help_text="Upload image to draw"
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.fullname} - {self.artstyle} ({self.status})"

    def is_pending(self):
        return self.status == 'Pending'

    def is_accepted(self):
        return self.status == 'Accepted'


# ===============================
# UPLOADED ART MODEL
# ===============================
class UploadedArt(models.Model):
    client_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20, blank=True, null=True)
    art = models.ImageField(upload_to='artworks/', null=True, blank=True)
    reference = models.ImageField(upload_to='references/', null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Uploaded Art"
        verbose_name_plural = "Uploaded Arts"
        ordering = ['-date_uploaded']

    def __str__(self):
        return f"{self.client_name} - {self.date_uploaded.strftime('%Y-%m-%d')}"


# ===============================
# APPOINTMENT FORM
# ===============================
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'fullname',
            'email',
            'contact',
            'date',
            'artstyle',
            'art_image',
            'payment_reference',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }