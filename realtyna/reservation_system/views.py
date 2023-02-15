from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Reservation, Listing
from .serializers import ReservationSerializer, AvailabilitySerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

@api_view(['POST'])
@csrf_exempt
def make_reservation(request):
    """
    API endpoint for making a reservation in a listing.
    Expects the following POST data:
    {
        "listing_id": 1,
        "name": "Shamim",
        "start_time": "2023-02-14T10:00:00Z",
        "end_time": "2023-02-14T11:00:00Z"
    }
    """
    data = request.data
    serializer = ReservationSerializer(data=data)
    if serializer.is_valid():
        # Check if any room in the listing is available for the given time period
        listing = get_object_or_404(Listing, id=request.data['listing_id'])
        reservation = Reservation.objects.filter(start_time__lte=data["end_time"], end_time__gte=data["start_time"], listing = listing.id).count()
        available_rooms = listing.num_rooms - reservation
        if available_rooms <= 0:
            return Response(
                {'error': 'No rooms are available for the given time period.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the reservation for the first available room
        reservation = serializer.save(listing=listing)
        
        # Return a response with the reservation details
        response_data = {
            'reservation_id': reservation.id,
            'listing_id': listing.id,
            'name': reservation.name,
            'start_time': reservation.start_time,
            'end_time': reservation.end_time,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])  # Specifies that this is a function-based view that accepts GET, PUT, and DELETE requests.
@csrf_exempt  # Exempts the view from CSRF protection.
def reservation(request, pk):
    """ Reservation system to Get, Update or Delete a reservation with ID"""
    # Retrieve the reservation object with the given pk or raise Http404 exception.
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'GET':
        # Serialize the reservation object using the ReservationSerializer.
        serializer = ReservationSerializer(reservation)
        # Return the serialized data as a JsonResponse.
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Deserialize the request data using the ReservationSerializer and update the reservation object.
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return the updated serialized data as a JsonResponse.
            return Response(serializer.data)
        # If the serializer is invalid, return the errors as a JsonResponse with HTTP 400 status code.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the reservation object.
        reservation.delete()
        # Return a HTTP 204 NO CONTENT response.
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@csrf_exempt
def check_availability(request):
    """ Check if we have room in a specific date"""
    # Retrieve query parameters from the request
    listing_id = request.GET.get('listing_id')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    
    # Query for the number of reservations that conflict with the requested times
    reservations = Reservation.objects.filter(start_time__lte=end_time, end_time__gte=start_time).count()
    
    # Retrieve the listing with the given ID
    listing = Listing.objects.get(id=listing_id)
    
    # Calculate the number of available rooms by subtracting the number of reservations from the total number of rooms
    count = listing.num_rooms - reservations
    
    # If there are available rooms, return a response with the number of rooms and a status of "available"
    if count > 0:
        serializer = AvailabilitySerializer({'available_rooms': count,'status':'available'})
        return JsonResponse(serializer.data)
    
    # If there are no available rooms, return a response with a count of 0 and a status of "unavailable"
    else:
        serializer = AvailabilitySerializer({'available_rooms': 0,'status':'unavailable'})
        return JsonResponse(serializer.data)


@api_view(['GET'])
@csrf_exempt
def booked_rooms_report(request):
    """ Return  reservation report"""
    # Get the listing ID from the request, if it exists
    listing_id = request.GET.get('listing_id')
    
    # If no listing ID is provided, get all reservations and order them by start time
    if not listing_id:
        reservations = Reservation.objects.all().order_by('start_time')
    # Otherwise, get only the reservations for the specified listing and order them by start time
    else:
        reservations = Reservation.objects.filter(listing=listing_id).order_by('start_time')
    
    # Render the booked_rooms_report.html template with the reservations data
    return render(request, 'booked_rooms_report.html', {'reservations': reservations})

    