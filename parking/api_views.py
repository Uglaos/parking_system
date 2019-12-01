from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import ParkingTicket

from .serializers import ParkingTicketSerializer, ParkingTicketPriceSerializer

import secrets
from datetime import datetime
from django.utils import timezone


class ParkingTicketCreate(APIView):

    def post(self, request):
        barcode = secrets.token_hex(16)[0:16]
        request.data.update(barcode=barcode)
        serializer_class = ParkingTicketSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save(barcode=barcode)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)


class ParkingTicketPrice(APIView):

    def get_ticket(self, barcode):
        if len(barcode) != 16:
            raise ValidationError({'barcode': 'Please enter valid barcode format!'})
        try:
            return ParkingTicket.objects.get(barcode=barcode)
        except ParkingTicket.DoesNotExist:
            raise ValidationError({'barcode': 'Ticket with this barcode does not exist!'})

    def get(self, request, barcode):
        ticket = self.get_ticket(barcode)
        serializer_class = ParkingTicketPriceSerializer(ticket)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)


class ParkingTicketPayment(APIView):

    def post(self, request, barcode):
        payment_option = request.data.get('payment_option')
        if payment_option is None:
            raise ValidationError({'payment_option': 'Please enter your payment_option!'})
        elif payment_option is not None and payment_option not in ['credit_card', 'debit_card', 'cash']:
            raise ValidationError({'payment_option': 'Your payment_option must be credit_card, debit_card or cash!'})
        ticket = ParkingTicketPrice.get_ticket(self, barcode)
        ticket.payment_option = payment_option
        ticket.paid = True
        ticket.paid_time = timezone.now()
        ticket.save()
        return Response(data={'ticket': 'paid'}, status=status.HTTP_200_OK)


class ParkingTicketState(APIView):

    def get(self, request, barcode):
        ticket = ParkingTicketPrice.get_ticket(self, barcode)
        diff = timezone.now() - ticket.paid_time
        if diff.seconds/60 > 15:
            ticket.paid = False
            ticket.start_time = timezone.now()
            ticket.save()
        if ticket.paid:
            return Response(data={'ticket': 'paid'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'ticket': 'unpaid'}, status=status.HTTP_200_OK)
