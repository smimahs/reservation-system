from django.urls import path
from . import views

urlpatterns = [
    path('api/reservations/', views.reservation),
    path('api/reservations/<int:pk>/', views.reservation_detail),
    path('api/reservations/available/', views.check_availability),
    path('api/reservations/report/', views.booked_rooms_report),
]
