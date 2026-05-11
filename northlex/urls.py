from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.accounts.urls')),
    path('dashboard/', include('apps.clients.urls')),
    path('advocate/', include('apps.advocates.urls')),
    path('admin-portal/', include('apps.admin_panel.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('cases/', include('apps.cases.urls')),
    path('chat/', include('apps.chat.urls')),
    path('payments/', include('apps.payments.urls')),
    path('feedback/', include('apps.feedback.urls')),
    path('northeast-hub/', include('apps.northeast_hub.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
