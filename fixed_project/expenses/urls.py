from django.urls import path
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # Default route
    path('', lambda request: redirect('login')),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Add expense
    path('add/', views.add_expense, name='add_expense'),

    # Budget
    path('set-budget/', views.set_budget, name='set_budget'),

    # Auth
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path("register/", views.register, name="register"),

    # Password
    path('change-password/', views.change_password, name='change_password'),

    # PDF
    path('export-pdf/', views.export_pdf, name='export_pdf'),

    # History
    path("history/", views.history, name="history"),
]
