from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render
from lazysignup.models import LazyUser
from lazysignup.utils import is_lazy_user


@staff_member_required
def overview(request):

    print User.objects.filter(lazyuser__isnull=True).count()
    for user in User.objects.all():
        print  is_lazy_user(user)

    return render(request, 'administration/overview.html',{

    })