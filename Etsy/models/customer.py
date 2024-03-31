from django.db import  models
from django.core.validators import MinLengthValidator

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return  False
    
    
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# models.py

email_regex = RegexValidator(regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', message="Please enter valid Email address.")
string_regex =  RegexValidator(regex=r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$', message="Some special characters like (~!#^`'$|{}<>*) are not allowed.")
mobile_validate = RegexValidator(regex=r'^(\+\d{1,3})?\d{10}$',message='Enter a valid 10-digit mobile number +91 9999999999')


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(
            username=username,
            # email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    USER_TYPE = (
        (1, "Customer"),
        (2, "Supplier"),
        (5 , "Store"),
        (7, "Admin"),
    )

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=50, null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    custom_user_role = models.IntegerField(choices=USER_TYPE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="deleted_by_user",
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="created_by_user",
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="updated_by_user",
        on_delete=models.CASCADE,
    )
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    fcm_token = models.CharField(verbose_name="FCM Token",max_length=250, blank=True, null=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    # REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Additional functionality to perform before saving
        if self.deleted_at and self.is_active:
            self.is_active = False
            # Add any other functionality you need here

        super().save(*args, **kwargs)

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def get_username(self):
        return self.username

    def __str__(self):
        return str(self.username)
    
    
class Supplier(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(unique=True,db_index=True, validators=[email_regex])
    first_name = models.CharField(max_length=50, blank=True, null=True, validators=[string_regex])
    last_name = models.CharField(max_length=50, blank=True, null=True,validators=[string_regex])
    phone_number = models.CharField(max_length=10, blank=True, null=True, validators=[mobile_validate])
    password = models.CharField(max_length=100)
    
    
class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(unique=True,db_index=True, validators=[email_regex])
    first_name = models.CharField(max_length=50, blank=True, null=True, validators=[string_regex])
    last_name = models.CharField(max_length=50, blank=True, null=True,validators=[string_regex])
    phone_number = models.CharField(max_length=10, blank=True, null=True, validators=[mobile_validate])
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email


