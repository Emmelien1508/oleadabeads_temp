from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not firstname: 
            raise ValueError("Users must have a firstname")
        if not lastname: 
            raise ValueError("Users must have a lastname")
        
        user = self.model(
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, firstname, lastname, password):
        user = self.create_user(
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email'), unique=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    streetname = models.CharField(max_length=30)
    housenr = models.CharField(max_length=30)
    postalcode = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin 
    
    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        if self.email:
            return self.email
        return f'Anonymous user'

class Color(models.Model):

    COLOR_CHOICES = (
        ('Wit', 'Wit'), 
        ('Blauw', 'Blauw'), 
        ('Oranje', 'Oranje'), 
        ('Paars', 'Paars'), 
        ('Roze', 'Roze'), 
        ('Rood', 'Rood'), 
        ('Parel', 'Parel'), 
        ('Edelsteen', 'Edelsteen'), 
        ('Beige', 'Beige'),
        ('Groen', 'Groen'),
        ('Geel', 'Geel')
    )

    color = models.CharField(max_length=30, choices=COLOR_CHOICES)

    def __str__(self):
        return self.color

class Photo(models.Model):
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.image.url  

class Product(models.Model):

    JEWELRY_CHOICES = (
        ('Armband', 'Armband'),
        ('Ketting', 'Ketting'),
        ('Oorbel', 'Oorbel'),
        ('Hanger', 'Hanger')
    )

    LOOK_CHOICES = (
        ('Kralen', 'Kralen'),
        ('Schakelketting', 'Schakelketting')
    )

    METAL_CHOICES = (
        ('RVS Goud', 'RVS Goud'),
        ('RVS Zilver', 'RVS Zilver'),
        ('Gold plated', 'Gold plated'),
        ('Silver plated', 'Silver plated')
    )

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    color = models.ManyToManyField(Color, blank=True)
    image = models.ManyToManyField(Photo)
    description = models.TextField()
    limited_edition = models.BooleanField(default=False)
    jewelry_type = models.CharField(max_length=30, choices=JEWELRY_CHOICES)
    look = models.CharField(max_length=30, choices=LOOK_CHOICES, blank=True, null=True)
    metal_type = models.CharField(max_length=30, choices=METAL_CHOICES)
    date_added = models.DateTimeField(default=now)
    size = models.IntegerField(blank=True, null=True)
    left = models.IntegerField()
    sale = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Diy(models.Model):

    JEWELRY_CHOICES = (
        ('Armband', 'Armband'),
        ('Ketting', 'Ketting'),
        ('Oorbellen', 'Oorbellen')
    )

    LOOK_CHOICES = (
        ('Kralen', 'Kralen'),
        ('Schakelketting', 'Schakelketting')
    )

    METAL_CHOICES = (
        ('RVS Goud', 'RVS Goud'),
        ('RVS Zilver', 'RVS Zilver'),
        ('Gold plated', 'Gold plated'),
        ('Silver plated', 'Silver plated')
    )

    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    color = models.ManyToManyField(Color)
    description = models.TextField()
    jewelry_type = models.CharField(max_length=30, choices=JEWELRY_CHOICES)
    look = models.CharField(max_length=30, choices=LOOK_CHOICES)
    metal_type = models.CharField(max_length=30, choices=METAL_CHOICES)

    def __str__(self):
        return f'{self.id}'

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    diyproduct = models.OneToOneField(Diy, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    ordered = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        if self.product:
            return f'{self.product.name}'
        return f'{self.diyproduct.id}'

class Order(models.Model):

    STATUS_CHOICES = (
        ('Verzonden', 'Verzonden'),
        ('In behandeling', 'In behandeling'),
        ('Ontvangen', 'Ontvangen')
    )

    SHIPPING_CHOICES = (
        ('Brievenbuspakketje', 'Brievenbuspakketje'),
        ('Met Track & Trace', 'Met Track & Trace')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    orderproduct = models.ManyToManyField(OrderProduct)
    date_ordered = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.TextField()
    shipping = models.CharField(max_length=50, choices=SHIPPING_CHOICES)
    free_shipping = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.email

class Favorite(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    favoriteproduct = models.ManyToManyField(Product)

    def __str__(self):
        return self.customer.email

class Discount(models.Model):
    DISCOUNT_CHOICES = (
        ('Vast bedrag', 'Vast bedrag'),
        ('Percentage', 'Percentage')
    )

    code = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField()
    discount_type = models.CharField(max_length=30, choices=DISCOUNT_CHOICES)
    discount_percentage = models.IntegerField(null=True)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return self.code

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer