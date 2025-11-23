from django.shortcuts import render,redirect
import requests

# Create your views here.
def main_page(request):
    return render(request, 'main_page/index.html')