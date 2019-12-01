from rest_framework import serializers
from parking.models import ParkingTicket


class ParkingTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingTicket
        fields = ('barcode', )
