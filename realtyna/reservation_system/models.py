from django.db import models

# Create your models here.
class Listing(models.Model):
    name = models.CharField(max_length=255)
    num_rooms = models.IntegerField()

class Reservation(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)