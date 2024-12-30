from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


AFRICAN_COUNTRIES = [
    ('DZ', 'Algeria'),
    ('AO', 'Angola'),
    ('BJ', 'Benin'),
    ('BW', 'Botswana'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('CM', 'Cameroon'),
    ('CV', 'Cape Verde'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('KM', 'Comoros'),
    ('CG', 'Congo (Brazzaville)'),
    ('CD', 'Congo (Kinshasa)'),
    ('CI', 'Côte d’Ivoire'),
    ('DJ', 'Djibouti'),
    ('EG', 'Egypt'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('ET', 'Ethiopia'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GH', 'Ghana'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'),
    ('KE', 'Kenya'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('ML', 'Mali'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('NA', 'Namibia'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('RW', 'Rwanda'),
    ('ST', 'São Tomé and Príncipe'),
    ('SN', 'Senegal'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('SS', 'South Sudan'),
    ('SD', 'Sudan'),
    ('SZ', 'Eswatini'),
    ('TZ', 'Tanzania'),
    ('TG', 'Togo'),
    ('TN', 'Tunisia'),
    ('UG', 'Uganda'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe'),
]

# Custom Account Manager
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        # Normalize email and create the user
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            is_admin=True,
            is_staff=True,
            is_superadmin=True,
            is_active=True
        )
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    # User Roles
    VENDOR = 'vendor'
    CUSTOMER = 'customer'
    ROLE_CHOICES = [
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    ]
 


        # Basic User Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    country_of_origin = models.CharField(max_length=2,choices=AFRICAN_COUNTRIES,blank=True,null=True)
    # Vendor-specific fields 
    
    store_name = models.CharField(max_length=100, blank=True, null=True)  # Only for vendors
    business_address = models.TextField(blank=True, null=True)  # Only for vendors
    vendor_documents = models.FileField(upload_to= 'vendors_docs/',blank = True,null = True)
    vendor_description = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=True)# True for now Till --to      changed
    vendor_images = models.ImageField(upload_to='photos/vendor_image')
    
    # Permissions and Status
    verification_status = models.CharField(
        max_length = 20,
        default = 'pending',
        choices = [('pending','Pending'),('verified','Verified'),('rejected','Rejected')]

    )
    #vendor verification 

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    # User login based on email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # Admin permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


    # Role-based checks
    @property
    def is_vendor(self):
        return self.role == self.VENDOR

    @property
    def is_customer(self):
        return self.role == self.CUSTOMER