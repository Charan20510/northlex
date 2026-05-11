from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache

from .models import OTPVerification
from .forms import MobileOTPRequestForm, OTPVerifyForm, RoleSelectForm, ProfileSetupForm
from .utils import send_otp_sms, normalize_mobile

User = get_user_model()


def landing(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())
    return render(request, 'accounts/landing.html')


@never_cache
@require_http_methods(['GET', 'POST'])
def otp_request(request):
    """Step 1: user enters mobile number, OTP is sent."""
    form = MobileOTPRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        mobile = form.cleaned_data['mobile']
        user, created = User.objects.get_or_create(
            mobile=mobile,
            defaults={'username': mobile, 'is_mobile_verified': False},
        )
        otp = OTPVerification.generate_otp(user, mobile)
        send_otp_sms(mobile, otp.otp_code)
        request.session['otp_mobile'] = mobile
        messages.info(request, f'OTP sent to {mobile}.')
        return redirect('accounts:otp_verify')
    return render(request, 'accounts/otp_request.html', {'form': form})


@never_cache
@require_http_methods(['GET', 'POST'])
def otp_verify(request):
    """Step 2: user enters OTP and gets logged in."""
    mobile = request.session.get('otp_mobile')
    if not mobile:
        return redirect('accounts:otp_request')

    form = OTPVerifyForm(request.POST or None, initial={'mobile': mobile})
    if request.method == 'POST' and form.is_valid():
        code = form.cleaned_data['otp_code']
        try:
            user = User.objects.get(mobile=mobile)
            otp = OTPVerification.objects.filter(
                user=user, mobile=mobile, is_used=False
            ).latest('created_at')
            if otp.is_valid() and otp.otp_code == code:
                otp.is_used = True
                otp.save()
                user.is_mobile_verified = True
                user.save(update_fields=['is_mobile_verified'])
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['otp_mobile']
                if not user.first_name:
                    return redirect('accounts:profile_setup')
                return redirect(user.get_dashboard_url())
            else:
                messages.error(request, 'Invalid or expired OTP. Try again.')
        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            messages.error(request, 'No OTP found. Please request a new one.')
    return render(request, 'accounts/otp_verify.html', {'form': form, 'mobile': mobile})


@never_cache
def resend_otp(request):
    mobile = request.session.get('otp_mobile')
    if not mobile:
        return redirect('accounts:otp_request')
    try:
        user = User.objects.get(mobile=mobile)
        otp = OTPVerification.generate_otp(user, mobile)
        send_otp_sms(mobile, otp.otp_code)
        messages.success(request, 'New OTP sent.')
    except User.DoesNotExist:
        messages.error(request, 'Mobile not registered.')
    return redirect('accounts:otp_verify')


def profile_setup(request):
    if not request.user.is_authenticated:
        return redirect('accounts:otp_request')
    user = request.user
    role_form = RoleSelectForm(request.POST or None)
    profile_form = ProfileSetupForm(request.POST or None, request.FILES or None, instance=user)
    if request.method == 'POST' and profile_form.is_valid() and role_form.is_valid():
        profile_form.save()
        user.role = role_form.cleaned_data['role']
        user.save(update_fields=['role'])
        messages.success(request, 'Profile created.')
        return redirect(user.get_dashboard_url())
    return render(request, 'accounts/profile_setup.html', {
        'profile_form': profile_form,
        'role_form': role_form,
    })


def logout_view(request):
    logout(request)
    return redirect('accounts:landing')
