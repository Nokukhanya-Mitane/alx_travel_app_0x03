import os
import uuid
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer
from .tasks import send_booking_confirmation_email


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        send_booking_confirmation_email.delay(
            booking.user.email,
            booking.id
        )


CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
CHAPA_INIT_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_VERIFY_URL = "https://api.chapa.co/v1/transaction/verify/"

@api_view(["POST"])
def initiate_payment(request):
    amount = request.data.get("amount")
    email = request.data.get("email")

    if not amount or not email:
        return Response(
            {"error": "Amount and email are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    tx_ref = str(uuid.uuid4())

    payload = {
        "amount": str(amount),
        "currency": "ETB",
        "email": email,
        "tx_ref": tx_ref,
        "callback_url": "http://localhost:8000/api/verify-payment/",
        "return_url": "http://localhost:3000/payment-success",
        "customization": {
            "title": "ALX Travel Booking",
            "description": "Booking payment"
        }
    }

    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(CHAPA_INIT_URL, json=payload, headers=headers)
    data = response.json()

    if response.status_code != 200 or not data.get("status"):
        return Response(
            {"error": "Payment initiation failed"},
            status=status.HTTP_400_BAD_REQUEST
        )

    Payment.objects.create(
        booking_reference=tx_ref,
        transaction_id=data["data"]["tx_ref"],
        amount=amount,
        status="Pending"
    )

    return Response(
        {
           
@api_view(["GET"])
def verify_payment(request):
    tx_ref = request.query_params.get("tx_ref")

    if not tx_ref:
        return Response(
            {"error": "Transaction reference required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET_KEY}"
    }

    response = requests.get(f"{CHAPA_VERIFY_URL}{tx_ref}", headers=headers)
    data = response.json()

    try:
        payment = Payment.objects.get(booking_reference=tx_ref)
    except Payment.DoesNotExist:
        return Response(
            {"error": "Payment record not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if data.get("status") == "success" and data["data"]["status"] == "success":
        payment.status = "Completed"
    else:
        payment.status = "Failed"

    payment.save()

    return Response(
        {
            "booking_reference": tx_ref,
            "status": payment.status
        },
        status=status.HTTP_200_OK
    )
