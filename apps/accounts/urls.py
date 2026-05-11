from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.otp_request, name='login'),
    path('login/otp/', views.otp_request, name='otp_request'),
    path('login/verify/', views.otp_verify, name='otp_verify'),
    path('login/resend/', views.resend_otp, name='resend_otp'),
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('logout/', views.logout_view, name='logout'),
]
