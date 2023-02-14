from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'name', 'start_time', 'end_time', 'listing_id')

class AvailabilitySerializer(serializers.Serializer):
    available_rooms = serializers.IntegerField()
    status = serializers.CharField()