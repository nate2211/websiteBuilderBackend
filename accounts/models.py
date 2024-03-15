from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import JSONField
from django.db import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=500,)
    about = models.TextField(max_length=2500,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class AccountImage(models.Model):
    account = models.ForeignKey(Account, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='account_images')

    def __str__(self):
        return f"Image of {self.account.username}"


class AccountLink(models.Model):
    account = models.ForeignKey(Account, related_name='links', on_delete=models.CASCADE)
    link = models.CharField(max_length=350)

    def __str__(self):
        return f"Link of {self.account.username}"


class AccountProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    account = models.ForeignKey(Account, related_name='%(class)ss', on_delete=models.CASCADE)
    class Meta:
        abstract = True

class DigitalProduct(AccountProduct):
    file = models.FileField(upload_to='digital_products')

    def __str__(self):
        return self.name

class PhysicalProduct(AccountProduct):
    weight = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

# New model AccountLayouts as requested
class AccountLayout(models.Model):
    PAGE_CHOICES = [
        ('shop', 'Shop'),
        ('contact', 'Contact'),
        ('about', 'About'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='layouts')
    page = models.CharField(max_length=10, choices=PAGE_CHOICES)
    layout = JSONField()

    class Meta:
        unique_together = ('account', 'page')  # Ensures one layout per page for each account

    def __str__(self):
        return f"Layout for {self.account.username} on {self.page}"