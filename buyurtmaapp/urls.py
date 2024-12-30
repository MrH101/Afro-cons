from django.urls import path
from .views import *

urlpatterns=[
    path('tanlangan/', TanlanganView.as_view(), name='tanlangan'),
    path('savat/', SavatView.as_view(), name='savat'),
    path('buyurtma/', BuyurtmaView.as_view(), name='buyurtma'),
]