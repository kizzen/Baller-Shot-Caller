from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404


# Create your views here.
def homepage(request):
    return render(request, 'baller_shot_caller/homepage.html')