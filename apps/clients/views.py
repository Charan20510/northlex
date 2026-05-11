from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import client_required

DASHBOARD_CARDS = [
    {'icon': '📋', 'label': 'Book an Advocate', 'url': '/bookings/book/', 'gradient': 'bg-gradient-to-br from-teal-400 to-primary'},
    {'icon': '⚖️', 'label': 'High Court Advocates', 'url': '/advocate/high-court/', 'gradient': 'bg-gradient-to-br from-blue-400 to-blue-600'},
    {'icon': '🏛️', 'label': 'Supreme Court (AOR)', 'url': '/advocate/supreme-court/', 'gradient': 'bg-gradient-to-br from-secondary to-blue-900'},
    {'icon': '📁', 'label': 'My Cases', 'url': '/cases/', 'gradient': 'bg-gradient-to-br from-green-400 to-green-600'},
    {'icon': '💬', 'label': 'Chat Support', 'url': '/chat/', 'gradient': 'bg-gradient-to-br from-purple-400 to-purple-600'},
    {'icon': '💳', 'label': 'Payments', 'url': '/payments/', 'gradient': 'bg-gradient-to-br from-amber-400 to-amber-600'},
    {'icon': '⭐', 'label': 'Feedback', 'url': '/feedback/', 'gradient': 'bg-gradient-to-br from-orange-400 to-orange-600'},
    {'icon': '🗺️', 'label': 'Northeast Law Hub', 'url': '/northeast-hub/', 'gradient': 'bg-gradient-to-br from-teal-500 to-green-500'},
    {'icon': '📞', 'label': 'Contact Admin', 'url': '/dashboard/contact-admin/', 'gradient': 'bg-gradient-to-br from-red-400 to-red-600'},
]


@login_required
@client_required
def dashboard(request):
    return render(request, 'dashboard/client_dashboard.html', {
        'dashboard_cards': DASHBOARD_CARDS,
    })
