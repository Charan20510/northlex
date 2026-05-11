from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPVerification


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'mobile', 'role', 'is_mobile_verified', 'is_approved', 'date_joined']
    list_filter = ['role', 'is_mobile_verified', 'is_approved']
    search_fields = ['username', 'mobile', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('NorthLex', {'fields': ('role', 'mobile', 'is_mobile_verified', 'is_approved', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('NorthLex', {'fields': ('role', 'mobile')}),
    )


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['mobile', 'otp_code', 'created_at', 'is_used']
    list_filter = ['is_used']
    search_fields = ['mobile']
    readonly_fields = ['otp_code', 'created_at']
