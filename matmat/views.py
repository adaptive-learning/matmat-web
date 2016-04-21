from django.shortcuts import render

from matmat import settings


def index(request):
    return render(request, "index.html", {
        "DEBUG": settings.DEBUG,
        "GOOGLE_ANALYTICS": settings.ON_SERVER,
    })
