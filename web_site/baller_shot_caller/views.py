from django.shortcuts import render
from django.http import HttpResponse

from .models import User

# Create your views here.
def homepage(request):
    users = User.objects.order_by('-join_date')[:5]
    output = ', '.join([q.name for q in users])
    return HttpResponse("Latest Baller Shot Caller users: " + output)

def user(request, user_id):
    user = User.objects.filter(id = user_id)
    return HttpResponse("%s's page" % user.first().name)