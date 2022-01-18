from django.urls import path
from .views import index, occupiedSeats, makeConfirmation, paymentConfirm, occupantInfo
app_name = 'movies'
urlpatterns = [
    path('', index, name="home"),
    path('occupied/', occupiedSeats, name="occupied_seat"),
    path('confirmation/', makeConfirmation, name="confirmation"),
    path('occupant_info/', occupantInfo, name="occupant_info"),
    #path('webhook/', webhook, name="webhook"),
    path('payment_confirm/', paymentConfirm, name="payment-confirm"),
]
