from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Reservation, Listing
from .serializers import ReservationSerializer, AvailabilitySerializer
from django.shortcuts import render
from rest_framework.parsers import JSONParser

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@csrf_exempt
def reservation(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReservationSerializer(data=data)        
        if serializer.is_valid():
            reservation = Reservation.objects.filter(start_time__lte=data["end_time"], end_time__gte=data["start_time"]).count()
            listing = Listing.objects.get(id=data["listing"])
            count = listing.num_rooms - reservation
            if count > 0:
                res = Reservation(name =data['name'],start_time = data['start_time'],end_time = data['end_time'],
                listing = listing)
                res.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({'Msg':"List is full! you can't reserve a room for this date!"}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ReservationSerializer(reservation, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        reservation.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def check_availability(request):
    if request.method == 'GET':
        listing_id = request.GET.get('listing_id')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        reservations = Reservation.objects.filter(start_time__lte=end_time, end_time__gte=start_time).count()
        listing = Listing.objects.get(id=listing_id)
        count = listing.num_rooms - reservations
        if count > 0:
            serializer = AvailabilitySerializer({'available_rooms': count,'status':'available'})
            return JsonResponse(serializer.data)
        else:
            serializer = AvailabilitySerializer({'available_rooms': 0,'status':'unavailable'})
            return JsonResponse(serializer.data)

@csrf_exempt
def booked_rooms_report(request):
    listing_id = request.GET.get('listing_id')
    if not listing_id:
        reservations = Reservation.objects.all().order_by('start_time')
    else:
        reservations = Reservation.objects.filter(listing=listing_id).order_by('start_time')
    return render(request, 'booked_rooms_report.html', {'reservations': reservations})
    