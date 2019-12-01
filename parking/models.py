from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

import math


def check_spaces():
    tickets = ParkingTicket.objects.filter(occupied=True)
    return len(tickets)


def get_ticket(barcode):
    if len(barcode) != 16:
        raise ValidationError({'barcode': 'Please enter valid barcode format!'})
    try:
        return ParkingTicket.objects.get(barcode=barcode)
    except ParkingTicket.DoesNotExist:
        raise ValidationError({'barcode': 'Ticket with this barcode does not exist!'})


class ParkingTicket(models.Model):

    def _get_ticket_price(self):
        diff = timezone.now() - self.start_time
        return math.ceil(diff.seconds/3600) * 2

    start_time = models.DateTimeField(auto_now_add=True)
    paid_time = models.DateTimeField(null=True)
    barcode = models.CharField(max_length=16)
    ticket_price = property(_get_ticket_price)
    paid = models.BooleanField(default=False)
    payment_option = models.CharField(max_length=11, null=True)
    occupied = models.BooleanField(default=False)
