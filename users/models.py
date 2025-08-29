from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqami '+998' bilan boshlanib, 12 ta raqamdan iborat bo‘lishi kerak."
)


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be set')
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.Roles.ADMIN)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('The superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('The superuser must have is_superuser=True.')
        return self.create_user(phone_number, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        RESTAURANT = "RESTAURANT", "Restaurant"
        COURIER = "COURIER", "Courier"

    username = models.CharField(max_length=20)
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return f"{self.username} ({self.phone_number})"
