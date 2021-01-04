from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
    )
from django.db import models
from django.db.models.signals import pre_save

from .utils import generate_token

import stripe

stripe.api_key = settings.STRIPE_SECRET

class UserManager(BaseUserManager):
    def create_user(self, email, first_name='', last_name='', password=None):
        if not email:
            raise ValueError('Email field is required')

        user = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name='', last_name='', password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='First Name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=30, blank=True)
    customer_id = models.CharField(verbose_name='Customer ID', max_length=255, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_admin = models.BooleanField(default=False, verbose_name='Admin')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Does the user have a specific permission, simply, yes
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class EmailToken(models.Model):
    token = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_tokens')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

# sending a signal to create a stripe customer and then associating it with a user
def user_customer_id_pre_save_signal(instance, *args, **kwargs):
    if not instance.customer_id:
        customer = stripe.Customer.create(
            email = instance.email
        )
        instance.customer_id = customer.id

pre_save.connect(user_customer_id_pre_save_signal, sender=User)

# sending a signal to create the email activation token
def email_token_pre_save_signal(instance, *args, **kwargs):
    if not instance.token:
        instance.token = generate_token()

pre_save.connect(email_token_pre_save_signal, sender=EmailToken)