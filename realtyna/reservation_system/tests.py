from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Listing, Reservation
from .serializers import AvailabilitySerializer, ReservationSerializer


class CheckAvailabilityTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.listing = Listing.objects.create(title='Test Listing', num_rooms=5)

    def test_check_availability(self):
        url = reverse('check-availability')
        data = {'listing_id': self.listing.id, 'start_time': '2023-03-01', 'end_time': '2023-03-05'}
        response = self.client.get(url, data)
        serializer = AvailabilitySerializer({'available_rooms': 5, 'status': 'available'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class ReservationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.listing = Listing.objects.create(title='Test Listing', num_rooms=5)
        self.reservation = Reservation.objects.create(
            listing=self.listing,
            guest_name='Test Guest',
            start_time='2023-03-01',
            end_time='2023-03-05'
        )

    def test_get_reservation(self):
        url = reverse('reservation-detail', args=[self.reservation.id])
        response = self.client.get(url)
        serializer = ReservationSerializer(self.reservation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_reservation(self):
        url = reverse('reservation-detail', args=[self.reservation.id])
        data = {'guest_name': 'New Guest'}
        response = self.client.put(url, data)
        self.reservation.refresh_from_db()
        serializer = ReservationSerializer(self.reservation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.reservation.guest_name, 'New Guest')

    def test_delete_reservation(self):
        url = reverse('reservation-detail', args=[self.reservation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

class MakeReservationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.listing = Listing.objects.create(title='Test Listing', num_rooms=5)

    def test_make_reservation(self):
        url = reverse('make-reservation')
        data = {
            'listing_id': self.listing.id,
            'guest_name': 'Test Guest',
            'start_time': '2023-03-01',
            'end_time': '2023-03-05'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Reservation.objects.filter(guest_name='Test Guest').exists())

