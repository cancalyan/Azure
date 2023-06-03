from django.shortcuts import render


def home(request):
    # Other code...
    return render(request, 'food/home.html')

def about(request):
    return render(request, 'food/about.html')
