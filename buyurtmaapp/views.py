from django.shortcuts import render, redirect
from django.views import View
from .models import *

class TanlanganView(View):
    def get(self, request):
        return render(request, 'page-profile-wishlist.html')

class SavatView(View):
    def get(self, request):
        return render(request, 'page-shopping-cart.html')

class BuyurtmaView(View):
    def get(self, request):
        return render(request, 'page-profile-orders.html')


