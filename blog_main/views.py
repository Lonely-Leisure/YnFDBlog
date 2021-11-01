from django.shortcuts import render

# Create your views here.


def nologin(request):
    return render(request, 'nologin.html')

