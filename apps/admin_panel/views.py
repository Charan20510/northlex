from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import admin_required


@login_required
@admin_required
def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')
