import json

from django.shortcuts import render

from matmat import settings


def index(request):
    return render(request, "index.html", {
        "user": json.dumps(request.user.userprofile.to_json()) if hasattr(request.user, "userprofile") else "",
        "DEBUG": settings.DEBUG,
        "GOOGLE_ANALYTICS": settings.ON_SERVER,
    })
