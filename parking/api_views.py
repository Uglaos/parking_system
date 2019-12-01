from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import ParkingTicket, check_available_spaces, get_ticket
from .serializers import ParkingTicketSerializer, ParkingTicketPriceSerializer

import secrets
from datetime import datetime
from django.utils import timezone


class ParkingTicketCreate(APIView):

    def post(self, request):
        if check_available_spaces() < 1:
            raise ValidationError({'parking': 'Not enough parking spaces!'})
        barcode = secrets.token_hex(16)[0:16]
        request.data.update(barcode=barcode)
        serializer_class = ParkingTicketSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save(barcode=barcode)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)


class ParkingTicketPrice(APIView):

    def get(self, request, barcode):
        ticket = get_ticket(barcode)
        serializer_class = ParkingTicketPriceSerializer(ticket)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)


class ParkingTicketPayment(APIView):

    def post(self, request, barcode):
        payment_option = request.data.get('payment_option')
        if payment_option is None:
            raise ValidationError({'payment_option': 'Please enter your payment_option!'})
        elif payment_option is not None and payment_option not in ['credit_card', 'debit_card', 'cash']:
            raise ValidationError({'payment_option': 'Your payment_option must be credit_card, debit_card or cash!'})
        ticket = get_ticket(barcode)
        ticket.payment_option = payment_option
        ticket.paid = True
        ticket.paid_time = timezone.now()
        ticket.save()
        return Response(data={'ticket': 'paid'}, status=status.HTTP_200_OK)


class ParkingTicketState(APIView):

    def get(self, request, barcode):
        ticket = get_ticket(barcode)
        diff = timezone.now() - ticket.paid_time
        if diff.seconds/60 > 15:
            ticket.paid = False
            ticket.start_time = timezone.now()
            ticket.save()
        if ticket.paid:
            return Response(data={'ticket': 'paid'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'ticket': 'unpaid'}, status=status.HTTP_200_OK)


class ParkingSpaces(APIView):

    def get(self, request):
        return Response(data={'spaces': check_available_spaces()})
