from django.contrib import admin

# Register your models here.
from .models import Reservation,Listing

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_time', 'end_time')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'num_rooms')

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Listing, ListingAdmin)