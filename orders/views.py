from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Order
from .forms import OrderCreateForm, OrderUpdateForm


# Customer Views
class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_customer:
            messages.error(request, "Only customers can place orders.")
            return redirect('home')

        form = OrderCreateForm()
        return render(request, 'orders/order_create.html', {'form': form})

    def post(self, request):
        if not request.user.is_customer:
            messages.error(request, "Only customers can place orders.")
            return redirect('home')

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            # Assign to a vendor (logic can be extended to choose vendor)
            order.vendor = request.user.vendor  # Assuming a relationship exists
            order.save()
            messages.success(request, "Your order has been placed.")
            return redirect('customer_orders')
        return render(request, 'orders/order_create.html', {'form': form})


class CustomerOrderListView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_customer:
            messages.error(request, "Only customers can view orders.")
            return redirect('home')

        orders = Order.objects.filter(customer=request.user).order_by('-created_at')
        return render(request, 'orders/customer_orders.html', {'orders': orders})


# Vendor Views
class VendorOrderListView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_vendor:
            messages.error(request, "Only vendors can manage orders.")
            return redirect('home')

        orders = Order.objects.filter(vendor=request.user).order_by('-created_at')
        return render(request, 'orders/vendor_orders.html', {'orders': orders})


class OrderUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, vendor=request.user)
        form = OrderUpdateForm(instance=order)
        return render(request, 'orders/order_update.html', {'form': form, 'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, vendor=request.user)
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order status has been updated.")
            return redirect('vendor_orders')
        return render(request, 'orders/order_update.html', {'form': form, 'order': order})
