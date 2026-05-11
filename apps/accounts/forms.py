from django import forms
from django.contrib.auth import get_user_model
from .utils import normalize_mobile

User = get_user_model()


class MobileOTPRequestForm(forms.Form):
    mobile = forms.CharField(max_length=15, label='Mobile Number')

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        return normalize_mobile(mobile)


class OTPVerifyForm(forms.Form):
    mobile = forms.CharField(widget=forms.HiddenInput)
    otp_code = forms.CharField(max_length=6, label='Enter OTP')

    def clean_otp_code(self):
        code = self.cleaned_data['otp_code'].strip()
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError('Enter the 6-digit OTP.')
        return code


class RoleSelectForm(forms.Form):
    role = forms.ChoiceField(
        choices=[('CLIENT', 'I need legal help'), ('ADVOCATE', 'I am an advocate')],
        widget=forms.RadioSelect,
        label='Register as',
    )


class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if email and qs.exists():
            raise forms.ValidationError('This email is already in use.')
        return email
