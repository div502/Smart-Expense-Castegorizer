import json
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash, logout
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from .models import Expense, Budget, CATEGORY_CHOICES
from .forms import ExpenseForm, BudgetForm


# ============================
# USER REGISTRATION
# ============================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! 🎉")
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# ============================
# USER LOGOUT (GET allowed)
# ============================
def logout_user(request):
    logout(request)
    return redirect('login')


# ============================
# CHANGE PASSWORD
# ============================
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully! 🔐")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'registration/change_password.html', {'form': form})


# ============================
# ADD EXPENSE
# ============================
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            messages.success(request, "Expense added successfully! 🎉")
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})


# ============================
# SET BUDGET
# ============================
@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            b = form.save(commit=False)
            b.user = request.user
            b.save()
            messages.success(request, "Budget saved successfully! 💰")
            return redirect('dashboard')
    else:
        form = BudgetForm()

    return render(request, 'expenses/set_budget.html', {'form': form})


# ============================
# EXPORT PDF
# ============================
@login_required
def export_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Expense_Report.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, 800, "Smart Expense Report")

    p.setFont("Helvetica", 12)
    y = 770
    p.drawString(40, y, f"User: {request.user.username}")
    y -= 30

    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Date")
    p.drawString(150, y, "Category")
    p.drawString(260, y, "Amount")
    p.drawString(350, y, "Description")
    y -= 20
    p.line(40, y, 550, y)
    y -= 20

    p.setFont("Helvetica", 11)
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    for e in expenses:
        p.drawString(40, y, str(e.date))
        p.drawString(150, y, e.category)
        p.drawString(260, y, f"₹{e.amount}")
        p.drawString(350, y, e.description[:35])
        y -= 20

        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 11)
            y = 800

    p.showPage()
    p.save()
    return response


# ============================
# HISTORY PAGE
# ============================
@login_required
def history(request):

    selected_date = request.GET.get("date", "")
    selected_category = request.GET.get("category", "")

    expenses = Expense.objects.filter(user=request.user)

    # DATE FILTER
    if selected_date:
        expenses = expenses.filter(date=selected_date)

    # CATEGORY FILTER
    if selected_category and selected_category != "All":
        expenses = expenses.filter(category=selected_category)

    # ORDER
    expenses = expenses.order_by("-date")

    # GROUP BY DATE
    grouped = {}
    for e in expenses:
        d = e.date.strftime("%d %B %Y")
        grouped.setdefault(d, []).append(e)

    return render(request, "expenses/history.html", {
        "grouped": grouped,
        "selected_date": selected_date,
        "selected_category": selected_category,
        "categories": CATEGORY_CHOICES,
    })


# ============================
# DASHBOARD
# ============================
@login_required
def dashboard(request):

    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('-date')

    # Total expenses
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # Monthly Chart Data
    monthly_qs = (
        expenses.extra({'month': "strftime('%%Y-%%m', date)"})
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    monthly_data = {i['month']: float(i['total']) for i in monthly_qs}

    # Category Chart Data
    category_qs = expenses.values('category').annotate(total=Sum('amount'))
    category_data = [
        {"category": c["category"], "total": float(c["total"])} for c in category_qs
    ]

    # Weekly Savings / Gamification
    today = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())
    weekly_total = Expense.objects.filter(
        user=user, date__gte=start_week
    ).aggregate(total=Sum('amount'))['total'] or 0

    weekly_budget = 2000
    weekly_savings = max(0, weekly_budget - weekly_total)

    gamification_msgs = []
    if weekly_savings > 0:
        gamification_msgs.append(f"Saved ₹{weekly_savings:.2f} this week! 🎉")

    # Streak Calculation
    daily_budget = 500
    streak = 0

    for i in range(1, 8):
        day = today - timedelta(days=i)
        day_total = Expense.objects.filter(
            user=user, date=day
        ).aggregate(total=Sum('amount'))['total'] or 0

        if day_total <= daily_budget:
            streak += 1
        else:
            break

    if streak > 0:
        gamification_msgs.append(f"{streak}-day under-budget streak! 🔥")

    # Suggestions
    this_month = today.replace(day=1)
    month_exp = Expense.objects.filter(user=user, date__gte=this_month)

    total_monthly = month_exp.aggregate(total=Sum('amount'))['total'] or 0
    food_spent = month_exp.filter(category="Food").aggregate(total=Sum('amount'))['total'] or 0

    suggestion = None
    if total_monthly > 0:
        percent = (food_spent / total_monthly) * 100
        if percent > 40:
            suggestion = f"🍔 Food spending is {percent:.1f}%. Try reducing!"

    # Budget Alerts
    budgets = Budget.objects.filter(user=user, month__month=today.month)
    alerts = []

    for b in budgets:
        spent = Expense.objects.filter(
            user=user,
            category=b.category,
            date__month=today.month
        ).aggregate(total=Sum('amount'))['total'] or 0

        if spent >= 0.8 * b.amount:
            alerts.append(
                f"⚠ You spent ₹{spent:.2f} of your {b.category} budget (Limit ₹{b.amount})"
            )

    return render(request, 'expenses/dashboard.html', {
        "expenses": expenses,
        "form": ExpenseForm(),
        "budget_form": BudgetForm(),
        "total_expenses": total_expenses,
        "monthly_data": json.dumps(monthly_data),
        "category_data": json.dumps(category_data),
        "gamification_msgs": gamification_msgs,
        "suggestion": suggestion,
        "alerts": alerts,
    })
