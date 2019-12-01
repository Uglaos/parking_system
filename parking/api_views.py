from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import ParkingTicket

from .serializers import ParkingTicketSerializer, ParkingTicketPriceSerializer

import secrets


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
