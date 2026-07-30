from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "title",
            "amount",
            "transaction_type",
            "category",
            "client_or_vendor",
            "payment_status",
            "payment_method",
            "upi_id",
            "reference_no",
            "due_date",
            "is_recurring",
            "note",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Example: Client payment / Office rent"}),
            "amount": forms.NumberInput(attrs={"placeholder": "Example: 5000", "step": "0.01"}),
            "transaction_type": forms.Select(),
            "category": forms.TextInput(attrs={"placeholder": "Example: Sales, Rent, Salary"}),
            "client_or_vendor": forms.TextInput(attrs={"placeholder": "Client or vendor name"}),
            "payment_status": forms.Select(),
            "payment_method": forms.Select(),
            "upi_id": forms.TextInput(attrs={"placeholder": "example@upi"}),
            "reference_no": forms.TextInput(attrs={"placeholder": "Bill / Invoice / Reference no"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 4, "placeholder": "Optional notes"}),
        }
