from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Category choices for expenses
CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Shopping', 'Shopping'),
    ('Utilities', 'Utilities'),
    ('Entertainment', 'Entertainment'),
    ('Transport', 'Transport'),
    ('Other', 'Other'),
]

class Expense(models.Model):
    """
    Model to store individual expense transactions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.category} - ₹{self.amount} on {self.date.strftime('%d-%m-%Y')}"


class Budget(models.Model):
    """
    Model to store monthly budget per category for each user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(default=timezone.now)  # stores month of the budget

    class Meta:
        # ensure unique budget for each user, category, and month (month+year only)
        unique_together = ('user', 'category', 'month')

    def __str__(self):
        return f"{self.user.username} - {self.category} Budget ₹{self.amount} ({self.month.strftime('%B %Y')})"
