from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    booked_seats = models.ManyToManyField('Seat', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} (${self.price})"


class Seat(models.Model):
    seat_no = models.IntegerField()
    occupant_first_name = models.CharField(max_length=255)
    occupant_last_name = models.CharField(max_length=255)
    occupant_email = models.EmailField(max_length=555)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    occupant_phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    purchase_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.occupant_first_name}-{self.occupant_last_name} seat_no {self.seat_no}"


class PaymentIntent(models.Model):
    #referrer = models.URLField()
    referrer = models.CharField(max_length=255, unique=True)
    movie_title = models.CharField(max_length=255)
    seat_number = models.CharField(max_length=200)


class Payment(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    movie = models.ForeignKey(
        Movie, on_delete=models.SET_NULL, null=True, blank=True)
    seat_no = models.IntegerField()
