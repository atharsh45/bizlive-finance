import csv
from decimal import Decimal
from urllib.parse import quote

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Transaction
from .forms import TransactionForm


def money(value):
    return Decimal(str(value or 0))


def get_stats():
    transactions = Transaction.objects.all().order_by("-id")

    income = Decimal("0.00")
    expense = Decimal("0.00")
    pending_income = Decimal("0.00")
    pending_expense = Decimal("0.00")
    upi_total = Decimal("0.00")
    razorpay_total = Decimal("0.00")
    overdue_amount = Decimal("0.00")
    today_net = Decimal("0.00")

    today = timezone.localdate()

    for t in transactions:
        amount = money(t.amount)

        if t.payment_status == "Paid":
            if t.transaction_type == "Income":
                income += amount
            else:
                expense += amount

            if t.paid_at and timezone.localtime(t.paid_at).date() == today:
                if t.transaction_type == "Income":
                    today_net += amount
                else:
                    today_net -= amount
        else:
            if t.transaction_type == "Income":
                pending_income += amount
            else:
                pending_expense += amount

        if t.payment_status == "Paid" and t.payment_method == "UPI":
            upi_total += amount

        if t.payment_status == "Paid" and t.payment_method == "Razorpay":
            razorpay_total += amount

        if t.payment_status != "Paid" and t.due_date and t.due_date < today:
            overdue_amount += amount

    balance = income - expense
    safe_to_spend = balance - pending_expense

    score = 100
    if balance < 0:
        score -= 40
    if pending_expense > income and pending_expense > 0:
        score -= 25
    if overdue_amount > 0:
        score -= 20
    if pending_income > income and pending_income > 0:
        score -= 10
    score = max(score, 0)

    if score >= 75:
        decision_status = "Stable"
    elif score >= 45:
        decision_status = "Control"
    else:
        decision_status = "Urgent"

    alerts = []
    if balance < 0:
        alerts.append("Expense is higher than income.")
    if overdue_amount > 0:
        alerts.append("Some pending payments are overdue.")
    if pending_income > 0:
        alerts.append("Pending income needs to be collected.")
    if pending_expense > 0:
        alerts.append("Pending expense needs to be paid.")
    if not alerts:
        alerts.append("Finance status looks good.")

    return {
        "transactions": transactions,
        "recent_transactions": transactions[:8],
        "income": income,
        "expense": expense,
        "balance": balance,
        "pending_income": pending_income,
        "pending_expense": pending_expense,
        "upi_total": upi_total,
        "razorpay_total": razorpay_total,
        "overdue_amount": overdue_amount,
        "safe_to_spend": safe_to_spend,
        "today_net": today_net,
        "score": score,
        "decision_status": decision_status,
        "alerts": alerts,
    }


def dashboard(request):
    context = get_stats()
    context["page"] = "dashboard"
    return render(request, "finance/dashboard.html", context)


def transactions_page(request):
    return render(request, "finance/transactions.html", {
        "transactions": Transaction.objects.all().order_by("-id"),
        "page": "transactions",
    })


def payments_page(request):
    return render(request, "finance/payments.html", {
        "transactions": Transaction.objects.all().order_by("-id"),
        "page": "payments",
    })


def reports(request):
    context = get_stats()
    context["page"] = "reports"
    return render(request, "finance/reports.html", context)


def upi_page(request):
    return render(request, "finance/upi.html", {
        "transactions": Transaction.objects.filter(payment_method="UPI").order_by("-id"),
        "page": "upi",
    })


def alerts_page(request):
    context = get_stats()
    context["page"] = "alerts"
    return render(request, "finance/alerts.html", context)


def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("transactions")
    else:
        form = TransactionForm()

    return render(request, "finance/form.html", {
        "form": form,
        "title": "Add Transaction",
        "page": "add",
    })


def edit_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("transactions")
    else:
        form = TransactionForm(instance=transaction)

    return render(request, "finance/form.html", {
        "form": form,
        "title": "Edit Transaction",
        "page": "transactions",
    })


def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.delete()
    return redirect("transactions")


def mark_paid(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.payment_status = "Paid"
    transaction.paid_at = timezone.now()
    if not transaction.reference_no:
        transaction.reference_no = f"MANUAL-{transaction.id}"
    transaction.save()
    return redirect("transactions")


def upi_pay_link(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    upi_id = transaction.upi_id or getattr(settings, "DEFAULT_UPI_ID", "")
    payee_name = transaction.client_or_vendor or "BizLive Finance"
    note = transaction.title or "Payment"

    if not upi_id:
        return HttpResponse("<h2>UPI ID missing</h2><a href='/transactions/'>Back</a>")

    upi_url = (
        "upi://pay?"
        f"pa={quote(upi_id)}"
        f"&pn={quote(payee_name)}"
        f"&am={transaction.amount}"
        f"&cu=INR"
        f"&tn={quote(note)}"
    )

    return render(request, "finance/upi_pay.html", {
        "transaction": transaction,
        "upi_url": upi_url,
        "upi_id": upi_id,
        "page": "upi",
    })


def create_payment(request, id):
    # This project uses demo checkout to avoid Razorpay account/key/pkg_resources errors.
    # Pay Now opens the same working demo payment page.
    return demo_payment_success(request, id)


@csrf_exempt
def payment_success(request):
    return redirect("transactions")


def demo_payment_success(request, id):
    transaction = get_object_or_404(Transaction, id=id)

    if request.method == "POST":
        selected_method = request.POST.get("payment_method", "Razorpay Demo")
        transaction.payment_status = "Paid"
        transaction.payment_method = "Razorpay"
        transaction.razorpay_order_id = f"demo_order_{transaction.id}"
        transaction.razorpay_payment_id = f"demo_{selected_method.lower().replace(' ', '_')}_{transaction.id}"
        transaction.reference_no = f"DEMO_REF_{transaction.id}"
        transaction.paid_at = timezone.now()
        transaction.save()

        return render(request, "finance/demo_payment_success.html", {
            "transaction": transaction,
            "selected_method": selected_method,
            "page": "payments",
        })

    return render(request, "finance/demo_payment.html", {
        "transaction": transaction,
        "page": "payments",
    })


def api_stats(request):
    stats = get_stats()
    return JsonResponse({
        "income": float(stats["income"]),
        "expense": float(stats["expense"]),
        "balance": float(stats["balance"]),
        "pending_income": float(stats["pending_income"]),
        "pending_expense": float(stats["pending_expense"]),
        "upi_total": float(stats["upi_total"]),
        "razorpay_total": float(stats["razorpay_total"]),
        "today_net": float(stats["today_net"]),
        "overdue_amount": float(stats["overdue_amount"]),
        "safe_to_spend": float(stats["safe_to_spend"]),
        "score": stats["score"],
        "decision_status": stats["decision_status"],
    })


def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Title", "Amount", "Type", "Category", "Client/Vendor", "Payment Status",
        "Payment Method", "UPI ID", "Reference No", "Due Date", "Paid At", "Note",
    ])

    for t in Transaction.objects.all().order_by("-id"):
        writer.writerow([
            t.title, t.amount, t.transaction_type, t.category, t.client_or_vendor,
            t.payment_status, t.payment_method, t.upi_id, t.reference_no,
            t.due_date, t.paid_at, t.note,
        ])

    return response
