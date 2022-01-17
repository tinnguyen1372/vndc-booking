from movies.tasks import mailing
from django.http.response import HttpResponse, HttpResponseForbidden
from movies.helpers import email_customer, verify_webook
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import requests
from .models import Movie, Seat, PaymentIntent, Payment
import uuid

from ipware import get_client_ip

# Create your views here.


def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {
        "movies": movies
    })


@csrf_exempt
def occupiedSeats(request):
    data = json.loads(request.body)

    movie = Movie.objects.get(title=data["movie_title"])
    occupied = movie.booked_seats.all()
    occupied_seat = list(map(lambda seat: seat.seat_no - 1, occupied))

    return JsonResponse({
        "occupied_seats": occupied_seat,
        "movie": str(movie)
    })


@csrf_exempt
def makeConfirmation(request):
    data = json.loads(request.body)
    seat_numbers = list(map(lambda seat: seat+1, data["seat_list"]))
    movie_title = data["movie_title"]

    cost = Movie.objects.get(title=movie_title).price

    referrer = uuid.uuid4().hex[:6].upper()
    # redirect_url = "/occupant_info/"
    redirect_url = "/payment_confirm/"
    PaymentIntent.objects.create(referrer=referrer,
                                 movie_title=movie_title,
                                 seat_number=seat_numbers)

    return JsonResponse({
        "payment_url": redirect_url,
        "referrer": referrer,
    })


@csrf_exempt
def occupantInfo(request):
    if request.method == "GET":
        referrer = request.GET.get('referrer', '')
        context = dict()
        context['referrer'] = referrer
        return render(request, "form.html", context=context)
    elif request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]

        referrer = request.POST["referrer"]
        print(referrer)

        payment_intent = PaymentIntent.objects.get(referrer=referrer)

        movie_title = payment_intent.movie_title
        movie = Movie.objects.get(title=movie_title)
        booked_seat = json.loads(payment_intent.seat_number)

        for seat_no in booked_seat:
            seat = Seat.objects.create(seat_no=seat_no,
                                       occupant_first_name=first_name,
                                       occupant_last_name=last_name,
                                       occupant_email=email)

            movie.booked_seats.add(seat)
            movie.save()

            Payment.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   email=email,
                                   phone=phone_number,
                                   movie=movie,
                                   seat_no=seat_no)

            # send email
            mailing.delay(first_name, email, seat_no, movie_title)
        return HttpResponse(200)

    return HttpResponseForbidden()


'''
@csrf_exempt
def webhook(request):
    if request.method == "POST":
        ip, is_routable = get_client_ip(request)

        if ip in settings.PAYSTACK_IP and verify_webook(request):
            response = json.loads(request.body)

            if response["event"] == "charge.success":
                first_name = response["data"]["customer"]["first_name"]
                last_name = response["data"]["customer"]['last_name']
                phone = response["data"]["customer"]['phone']
                email = response["data"]["customer"]['email']
                amount = int(response["data"]["amount"])

                referrer = response["data"]["metadata"]["referrer"]

                payment_intent = PaymentIntent.objects.get(referrer=referrer)

                movie_title = payment_intent.movie_title
                movie = Movie.objects.get(title=movie_title)
                booked_seat = json.loads(payment_intent.seat_number)

                for seat_no in booked_seat:
                    seat = Seat.objects.create(seat_no=seat_no,
                                               occupant_first_name=first_name,
                                               occupant_last_name=last_name,
                                               occupant_email=email)

                    movie.booked_seats.add(seat)
                    movie.save()

                    Payment.objects.create(first_name=first_name,
                                           last_name=last_name,
                                           email=email,
                                           phone=phone,
                                           movie=movie,
                                           seat_no=seat_no)

                    # send email
                    #mailing.delay(first_name, email, seat_no, movie_title)
                return HttpResponse(200)

    return HttpResponseForbidden()
'''


def paymentConfirm(request):
    # return HttpResponse('<h2>Thank you for purchasing Us....</h2>\n\
    #     <h2>An email has been sent to your email address with your seat number</h2>\n\
    #     <h2>Thank you once again</h2>\n\
    #     <a href="/" >Click here to go to homepage</a>')
    render(request, 'confirmation.html')
