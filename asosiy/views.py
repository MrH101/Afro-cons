'''from django.shortcuts import render, redirect
from django.views import View

from .models import *


class HomeIndex2View(View):
    def get(self, request):
        data={
            'bolimlar': Bolim.objects.all()[:6]
        }
        return render(request, 'page-index-2.html', data)


class HomeIndex(View):

    def get(self, request):
        if request.user.is_authenticated:
            data={
                'bolimlar': Bolim.objects.all()[:6],
                'davomi': Bolim.objects.all()[6:]
            }
            return render(request, 'page-index.html', data)
        return redirect('/user/login/')

class BolimlarView(View):
    def get(selfself, request):
        data={
           'bolimlar': Bolim.objects.all()
        }
        return render(request, 'page-category.html', data)

class ListingGridView(View):
    def get(self,request, son):
        mahsulotlar=Mahsulot.objects.filter(ichki__id=son)
        data={
            'mahsulotlar': mahsulotlar
        }
        return render(request,'page-listing-grid.html', data)

class DetailProductView(View):
    def get(self,request, son):
        data={
            'mahsulot': Mahsulot.objects.get(id=son)
        }
        return render(request,'page-detail-product.html', data)

class IchkiView(View):
    def get(self, request, nom):
        data={
            'bolim': Bolim.objects.get(nom=nom),
            'ichkilar': Ichki.objects.filter(bolim__nom=nom)
        }
        return render(request, 'ichki.html', data)
'''
'''from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models import Product, Category  # Assuming 'store' is the app where Product and Category models are defined

class HomeIndex2View(View):
    def get(self, request):
        data = {
            'categories': Category.objects.all()[:6],  # Display first 6 categories
            'products': Product.objects.filter(is_available=True),  # Display 10 featured products
        }
        return render(request, 'page-index-2.html', data)


class HomeIndex(View):
    def get(self, request):
        if request.user.is_authenticated:
            data = {
                'categories': Category.objects.all()[:6],  # Display first 6 categories
                'more_categories': Category.objects.all()[6:],  # Display remaining categories
                'latest_products': Product.objects.filter(is_available=True).order_by('-created_date')[:10],  # Show latest 10 products
                'featured_products': Product.objects.filter(is_available=True)[:10],  # Show 10 featured products
            }
            return render(request, 'page-index-2.html', data)
        return redirect('/user/login/')


class CategoryView(View):
    def get(self, request):
        data = {
            'categories': Category.objects.all(),  # Display all categories
        }
        return render(request, 'page-category.html', data)


class ListingGridView(View):
    def get(self, request, category_id):
        products = Product.objects.filter(category__id=category_id, is_available=True)
        data = {
            'products': products,
            'category': get_object_or_404(Category, id=category_id)
        }
        return render(request, 'page-listing-grid.html', data)


class DetailProductView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_available=True)
        data = {
            'product': product
        }
        return render(request, 'page-detail-product.html', data)


class IchkiView(View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = category.subcategory_set.all()  # Assuming each category has subcategories
        data = {
            'category': category,
            'subcategories': subcategories
        }
        return render(request, 'ichki.html', data)

'''