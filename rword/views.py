from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import WordList
from .models import SentenceList

# Create your views here.

def rwordpage(request):
    if request.GET.get('button2')=="2":
        rwordlist = WordList.objects.order_by('?')[:2]
    elif request.GET.get('button3')=="3":
        rwordlist = WordList.objects.order_by('?')[:3]
    elif request.GET.get('button4')=="4":
        rwordlist = WordList.objects.order_by('?')[:4]
    else:
        rwordlist = 'click button'
    return render(request, 'rwordpage.html', {'rwordlist':rwordlist})

def insertsentence(request):
    if request.method == 'POST':
        s = SentenceList.objects.Create(sentence=request.POST['insentence'])
        s.save()
    return render(request, 'rwordpage.html')

    
def rwordboard(request):
    
    return render(request, 'rwordboard.html')