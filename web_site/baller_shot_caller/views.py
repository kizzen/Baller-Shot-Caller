from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import User

# Create your views here.
def homepage(request):
    user_list = User.objects.order_by('-join_date')[:5]
    context = {
        'user_list': user_list,
    }
    return render(request, 'baller_shot_caller/homepage.html', context)

def user(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    return render(request, 'baller_shot_caller/user.html', {'user': user})
