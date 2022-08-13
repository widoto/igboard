from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import WordList

# Create your views here.

def rwordpage(request):
    rwordlist = WordList.objects.order_by('?')[:2]
    return render(request, 'rwordpage.html', {'rwordlist':rwordlist})