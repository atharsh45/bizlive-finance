from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("transactions/", views.transactions_page, name="transactions"),
    path("payments/", views.payments_page, name="payments"),
    path("reports/", views.reports, name="reports"),
    path("upi/", views.upi_page, name="upi_page"),
    path("alerts/", views.alerts_page, name="alerts"),

    path("add/", views.add_transaction, name="add_transaction"),
    path("edit/<int:id>/", views.edit_transaction, name="edit_transaction"),
    path("delete/<int:id>/", views.delete_transaction, name="delete_transaction"),
    path("mark-paid/<int:id>/", views.mark_paid, name="mark_paid"),

    path("upi-pay/<int:id>/", views.upi_pay_link, name="upi_pay_link"),

    path("pay/<int:id>/", views.create_payment, name="create_payment"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("demo-pay/<int:id>/", views.demo_payment_success, name="demo_payment_success"),

    path("api/stats/", views.api_stats, name="api_stats"),
    path("export-csv/", views.export_csv, name="export_csv"),
]
