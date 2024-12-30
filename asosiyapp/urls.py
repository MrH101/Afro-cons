from django.urls import path
from .views import *

urlpatterns=[
    path('', HomeIndex.as_view(), name='home'),
    path('home/', HomeIndex2View.as_view(), name='home2'),
    path('bolimlar/', CategoryView.as_view(), name='categories'),
    path('ichki/<int:son>/mahsulotlar/', ListingGridView.as_view(), name='listinggrid'),
    path('mahsulot/<int:son>/', DetailProductView.as_view(), name='detailp'),
    path('bolim/<str:nom>/', IchkiView.as_view(), name='ichki'),
]