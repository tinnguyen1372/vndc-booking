import hmac
import hashlib
from django.conf import settings

from django.template.loader import render_to_string
from django.core.mail import send_mail


# def verify_webook(request):
#     secret = bytes(settings.PAYSTACK_SECRET, "utf-8")
#     digester = hmac.new(secret, request.body, hashlib.sha512)
#     calculated_signature = digester.hexdigest()
#     if calculated_signature == request.META["HTTP_X_PAYSTACK_SIGNATURE"]:
#         return True
#     return False

from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage


def email_customer(first_name, seat_no, movie_title, email):
    d = {
        2: 'A18', 3: 'A17', 4: 'A16', 5: 'A15', 6: 'A14', 7: 'A13', 8: 'A12', 9: 'A11', 10: 'A10', 11: 'A9', 12: 'A8', 13: 'A7', 14: 'A6', 15: 'A5', 16: 'A4', 17: 'A3', 18: 'A2', 19: 'A1',
        24: 'B18', 25: 'B17', 26: 'B16', 27: 'B15', 28: 'B14', 29: 'B13', 30: 'B12', 31: 'B11', 32: 'B10', 33: 'B9', 34: 'B8', 35: 'B7', 36: 'B6', 37: 'B5', 38: 'B4', 39: 'B3', 40: 'B2', 41: 'B1',
        46: 'C18', 47: 'C17', 48: 'C16', 49: 'C15', 50: 'C14', 51: 'C13', 52: 'C12', 53: 'C11', 54: 'C10', 55: 'C9', 56: 'C8', 57: 'C7', 58: 'C6', 59: 'C5', 60: 'C4', 61: 'C3', 62: 'C2', 63: 'C1',
        68: 'D18', 69: 'D17', 70: 'D16', 71: 'D15', 72: 'D14', 73: 'D13', 74: 'D12', 75: 'D11', 76: 'D10', 77: 'D9', 78: 'D8', 79: 'D7', 80: 'D6', 81: 'D5', 82: 'D4', 83: 'D3', 84: 'D2', 85: 'D1',
        90: 'E18', 91: 'E17', 92: 'E16', 93: 'E15', 94: 'E14', 95: 'E13', 96: 'E12', 97: 'E11', 98: 'E10', 99: 'E9', 100: 'E8', 101: 'E7', 102: 'E6', 103: 'E5', 104: 'E4', 105: 'E3', 106: 'E2', 107: 'E1',
        110: 'F22', 111: 'F21', 112: 'F20', 113: 'F19', 114: 'F18', 115: 'F17', 116: 'F16', 117: 'F15', 118: 'F14', 119: 'F13', 120: 'F12', 121: 'F11', 122: 'F10', 123: 'F9', 124: 'F8', 125: 'F7', 126: 'F6', 127: 'F5',
        128: 'F4', 129: 'F3', 130: 'F2', 131: 'F1'
    }
    # render_msg = render_to_string("email_template.html", {
    #     "first_name": first_name,
    #     "movie_title": movie_title,
    #     "seat_no": d[seat_no-1]
    # })

    # send_mail(
    #     "[VNDC XXII]: Xác nhận đặt vé thành công",
    #     render_msg,
    #     settings.EMAIL_HOST_USER, 
    #     [email, ],

    # )
    message = get_template("email_template.html").render(Context({
            "first_name": first_name,
            "movie_title": movie_title,
            "seat_no": d[seat_no-1]
    }))
    mail = EmailMessage(
        subject="[VNDC XXII]: Xác nhận đặt vé thành công",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    return mail.send()


