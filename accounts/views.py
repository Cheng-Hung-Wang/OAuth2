from django.shortcuts import render

# Create your views here.

from oauth2.views import callback
from oauth2.views import GoogleOAuth2
from django.http import HttpResponse

def login(request):
    return GoogleOAuth2().authorize(request)


def callback(request):
    data = GoogleOAuth2().credential(request)
    return HttpResponse(str(data))

