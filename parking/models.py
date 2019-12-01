from django.db import models


class ParkingTicket(models.Model):

    start_time = models.DateTimeField(auto_now_add=True)
    barcode = models.CharField(max_length=16)
