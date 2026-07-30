from django.db import models


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("Income", "Income"),
        ("Expense", "Expense"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Payment Started", "Payment Started"),
        ("Payment Failed", "Payment Failed"),
    ]

    METHOD_CHOICES = [
        ("Razorpay", "Razorpay"),
        ("UPI", "UPI"),
        ("Cash", "Cash"),
        ("Bank Transfer", "Bank Transfer"),
        ("Card", "Card"),
        ("Cheque", "Cheque"),
    ]

    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="Income")
    category = models.CharField(max_length=80, blank=True)
    client_or_vendor = models.CharField(max_length=120, blank=True)
    payment_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default="Razorpay")
    upi_id = models.CharField(max_length=120, blank=True)
    reference_no = models.CharField(max_length=120, blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    razorpay_order_id = models.CharField(max_length=120, blank=True)
    razorpay_payment_id = models.CharField(max_length=120, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)

    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
