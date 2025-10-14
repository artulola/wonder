from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/base.html')