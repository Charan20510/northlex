from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import advocate_required


@login_required
@advocate_required
def dashboard(request):
    return render(request, 'advocates/dashboard.html')
