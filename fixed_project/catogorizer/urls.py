# catogorizer/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django built-in Authentication (login, logout, password reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # Your Expense application routes
    path('', include('expenses.urls')),   # include ONLY ONCE
]
