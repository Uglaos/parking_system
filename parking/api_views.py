from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ParkingTicketSerializer

import secrets


class ParkingTicketCreate(APIView):

    def post(self, request):
        barcode = secrets.token_hex(16)[0:16]
        request.data.update(barcode=barcode)
        serializer_class = ParkingTicketSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save(barcode=barcode)
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)
