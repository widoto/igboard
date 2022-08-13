from django.shortcuts import render

# Create your views here.
def rwordpage(request):
    return render(request, 'rwordpage.html')