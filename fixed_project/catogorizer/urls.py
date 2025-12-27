# catogorizer/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
import json

def manifest_view(request):
    """Serve the PWA manifest file"""
    with open(settings.BASE_DIR / 'static' / 'manifest.json', 'r') as f:
        manifest_data = json.load(f)
    return HttpResponse(json.dumps(manifest_data), content_type='application/json')

def sw_view(request):
    """Serve the service worker file"""
    with open(settings.BASE_DIR / 'static' / 'sw.js', 'r') as f:
        sw_content = f.read()
    return HttpResponse(sw_content, content_type='application/javascript')

urlpatterns = [
    path('admin/', admin.site.urls),

    # PWA files
    path('manifest.json', manifest_view, name='manifest'),
    path('sw.js', sw_view, name='sw'),

    # Django built-in Authentication (login, logout, password reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # Your Expense application routes
    path('', include('expenses.urls')),   # include ONLY ONCE
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
