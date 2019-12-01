from django.db import models
from django.utils import timezone

import math


class ParkingTicket(models.Model):

    def _get_ticket_price(self):
        diff = timezone.now() - self.start_time
        return math.ceil(diff.seconds/3600) * 2

    start_time = models.DateTimeField(auto_now_add=True)
    barcode = models.CharField(max_length=16)
    ticket_price = property(_get_ticket_price)
