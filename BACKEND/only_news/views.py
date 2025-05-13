from django.shortcuts import render

def home_onlyNews(request):
    return render(request, 'home.html')