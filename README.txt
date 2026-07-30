BizLive - Final Correct Django HTML Finance Project

This is a clean fixed Django + HTML + CSS project.

Features:
- Dashboard
- Add/Edit/Delete Transactions
- Pending Income and Pending Expense
- Razorpay Total card
- UPI Total card
- Demo Pay page
- Mark Paid
- Reports
- Alerts
- CSV Export

Run steps in VS Code PowerShell:

1) Open this folder in VS Code.

2) Run:
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations finance
python manage.py migrate
python manage.py runserver

3) Open:
http://127.0.0.1:8000/

Demo Payment test:
- Add transaction
- Payment Status: Pending
- Payment Method: Razorpay
- Open Transactions
- Click Demo Pay
- Select option and Pay

Note:
This version avoids the Razorpay pkg_resources error. Real Razorpay login/key is not required for demo.
