from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect ,get_object_or_404
from django.views import View
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import VendorVerificationForm,LoginForm
from .models import Account 
from store.models import Product 

class LoginView(View):
    def get(self, request):
        # Instantiate an empty form for the GET request
        form = LoginForm()
        return render(request, 'user-login.html', {'form': form})

    def post(self, request):
        # Bind the form with POST data
        form = LoginForm(request, data=request.POST)

        # Validate the form
        if form.is_valid():
            # Authenticate and log in the user
            user = form.get_user()  # This method comes from AuthenticationForm

            if user is not None:
                login(request, user)  # Log in the user

                # Redirect based on user role
                if user.is_vendor:
                    return redirect('vendor_dashboard')
                elif user.is_customer:
                    return redirect('home')
                else:
                    return redirect('home')
            else:
                # If authentication failed (shouldn't reach here if form is valid)
                messages.error(request, "Invalid login credentials.")
                return redirect('login')
        else:
            # If form is invalid, re-render the login page with the form and errors
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'user-login.html', {'form': form})



class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('/user/login/')


class VendorRegisterView(View):
    def get(self, request):
        form = VendorSignUpForm()
        return render(request, 'vendor/register.html', {'form': form})

    def post(self, request):
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your vendor account has been created. You will be able to log in after verification.")
            return redirect('login')
        return render(request, 'vendor/register.html', {'form': form})


class CustomerRegisterView(View):
    def get(self, request):
        form = CustomerSignUpForm()
        return render(request, 'customer/register.html', {'form': form})

    def post(self, request):
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your customer account has been created. You can now log in.")
            return redirect('login')
        return render(request, 'customer/register.html', {'form': form})


# Refactor vendor_verification into a class-based view using UpdateView
class VendorVerificationView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = VendorVerificationForm
    template_name = 'vendor/verification.html'
    success_url = reverse_lazy('vendor_dashboard')

    def get_object(self, queryset=None):
        # Ensure the user updating the form is the logged-in user
        return self.request.user

    def form_valid(self, form):
        # Check if the user is a vendor
        if not self.request.user.is_vendor:
            messages.error(self.request, "You must be a vendor to submit verification documents.")
            return redirect('home')  # Redirect to homepage or dashboard

        # Save form and update status to 'pending'
        form.instance.verification_status = 'pending'
        messages.success(self.request, "Your documents have been submitted for verification.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please try again.")
        return super().form_invalid(form)


# Vendor Dashboard
class VendorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'vendor/dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_vendor:
            messages.error(request, "You do not have access to the vendor dashboard.")
            return redirect('home')
        return super().get(request, *args, **kwargs)


# Customer Dashboard
class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_customer:
            messages.error(request, "You do not have access to the customer dashboard.")
            return redirect('home')
        return super().get(request, *args, **kwargs)


class VendorDetailView(View):
    def get(self,request,username):
        vendor = get_object_or_404(Account,username=username,role=Account.VENDOR)
        products = Product.objects.filter(vendor = vendor)
        return render(request,'store/vendor_detail.html',{'vendor':vendor,'products':products})
