import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'CLIENT', 'Client'
        ADVOCATE = 'ADVOCATE', 'Advocate'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT

    @property
    def is_advocate(self):
        return self.role == self.Role.ADVOCATE

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def get_dashboard_url(self):
        if self.role == self.Role.ADVOCATE:
            return '/advocate/dashboard/'
        if self.role == self.Role.ADMIN:
            return '/admin-portal/'
        return '/dashboard/'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.role})'


class OTPVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otps')
    mobile = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def generate_otp(cls, user, mobile):
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        code = str(random.randint(100000, 999999))
        return cls.objects.create(user=user, mobile=mobile, otp_code=code)

    def is_valid(self):
        expiry = self.created_at + timedelta(minutes=10)
        return not self.is_used and timezone.now() <= expiry

    def __str__(self):
        return f'OTP for {self.mobile} — {"used" if self.is_used else "active"}'
