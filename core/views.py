from django.shortcuts import render
from lazysignup.decorators import allow_lazy_user


@allow_lazy_user
def home(request):
    return render(request, 'core/home.html')