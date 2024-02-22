from django.shortcuts import render
from zarinpal import PaymentGateway

def initiate_payment(request):
    if request.method == 'POST':
        gateway = PaymentGateway(MERCHANT_ID, 'https://yourwebsite.com/payment/verify/')
        amount = 1000  # Amount in Toman
        description = 'Payment for services'
        result = gateway.send_request(amount, description)
        if result.get('Status') == 100:
            return redirect(result.get('StartPay'))
        else:
            return render(request, 'payment_failed.html')
    return render(request, 'initiate_payment.html')
