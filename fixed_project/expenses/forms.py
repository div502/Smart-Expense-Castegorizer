from django import forms
from .models import Expense, Budget, CATEGORY_CHOICES


# ============================
# EXPENSE FORM (Fixed + Styled)
# ============================
class ExpenseForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=[("", "Select Category")] + CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            "class": "w-full p-2 border rounded-lg bg-gray-100 dark:bg-gray-700 dark:text-white"
        })
    )

    class Meta:
        model = Expense
        fields = ["amount", "category", "description", "date"]

        widgets = {
            "amount": forms.NumberInput(attrs={
                "step": "0.01",
                "placeholder": "Enter amount",
                "class": "w-full p-2 border rounded-lg bg-gray-100 dark:bg-gray-700 dark:text-white"
            }),

            "description": forms.TextInput(attrs={
                "placeholder": "Write description…",
                "class": "w-full p-2 border rounded-lg bg-gray-100 dark:bg-gray-700 dark:text-white"
            }),

            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full p-2 border rounded-lg bg-gray-100 dark:bg-gray-700 dark:text-white"
            }),
        }


# ============================
# BUDGET FORM (Fixed + Styled)
# ============================
class BudgetForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=[("", "Select Category")] + CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            "class": "w-full p-2 border rounded-lg bg-gray-100 dark:bg-gray-700 dark:text-white"
        })
    )

    class Meta:
        model = Budget
        fields = ["category", "amount", "month"]

        widgets = {
            "amount": forms.NumberInput(attrs={
                "step": "0.01",
                "placeholder": "Enter monthly limit",
                "class": "w-full p-2 border rounded-lg bg-gray-100 dark:bg-gray-700 dark:text-white"
            }),

            "month": forms.DateInput(attrs={
                "type": "month",
                "class": "w-full p-2 border rounded-lg bg-gray-100 dark:bg-gray-700 dark:text-white"
            }),
        }
