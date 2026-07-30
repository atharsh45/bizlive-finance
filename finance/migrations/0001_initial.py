# Generated for BizLive final project

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("transaction_type", models.CharField(choices=[("Income", "Income"), ("Expense", "Expense")], default="Income", max_length=20)),
                ("category", models.CharField(blank=True, max_length=80)),
                ("client_or_vendor", models.CharField(blank=True, max_length=120)),
                ("payment_status", models.CharField(choices=[("Pending", "Pending"), ("Paid", "Paid"), ("Payment Started", "Payment Started"), ("Payment Failed", "Payment Failed")], default="Pending", max_length=30)),
                ("payment_method", models.CharField(choices=[("Razorpay", "Razorpay"), ("UPI", "UPI"), ("Cash", "Cash"), ("Bank Transfer", "Bank Transfer"), ("Card", "Card"), ("Cheque", "Cheque")], default="Razorpay", max_length=30)),
                ("upi_id", models.CharField(blank=True, max_length=120)),
                ("reference_no", models.CharField(blank=True, max_length=120)),
                ("due_date", models.DateField(blank=True, null=True)),
                ("is_recurring", models.BooleanField(default=False)),
                ("note", models.TextField(blank=True)),
                ("razorpay_order_id", models.CharField(blank=True, max_length=120)),
                ("razorpay_payment_id", models.CharField(blank=True, max_length=120)),
                ("razorpay_signature", models.CharField(blank=True, max_length=255)),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
