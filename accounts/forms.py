from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Account

class VendorVerificationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['store_name', 'business_address', 'vendor_documents', 'vendor_description']
        widgets = {
            'store_name': forms.TextInput(attrs={'placeholder': 'Enter your store name'}),
            'business_address': forms.Textarea(attrs={'placeholder': 'Enter your business address'}),
            'vendor_description': forms.Textarea(attrs={'placeholder': 'Describe your business'}),
        }
        labels = {
            'vendor_documents': 'Upload Company Documents',
        }

# Vendor Sign-Up Form
class VendorSignUpForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2', 'store_name', 'business_address']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'store_name': forms.TextInput(attrs={'placeholder': 'Enter your store name'}),
            'business_address': forms.Textarea(attrs={'placeholder': 'Enter your business address'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Account.VENDOR  # Set the user role to 'vendor' during sign-up
        user.is_active = False  # Vendor will be inactive until verification
        if commit:
            user.save()
        return user

# Customer Sign-Up Form
class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Account.CUSTOMER  # Set the user role to 'customer' during sign-up
        user.is_active = True  # Customers are active by default
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control'}),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}),
        label="Password",
    )

    class Meta:
        model = Account
        fields = ['username', 'password']

    def confirm_login_allowed(self, user):
        """
        Override the confirm_login_allowed method to ensure that only active users can log in.
        This method could also be used to check any additional conditions before allowing login.
        """
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive. Please contact support.",
                code='inactive',
            )