from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from .base import BaseUUIDTimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        """
        Creates and saves a User with the given email, full_name and password
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not full_name:
            raise ValueError('Users must have a full name')

        user = self.model(email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.is_email_verified = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        """
        Creates and saves a superuser with the given email, full_name and password
        """
        user = self.create_user(email, password=password, full_name=full_name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(BaseUUIDTimeStampedModel, AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    profile_url = models.CharField(max_length=200, blank=True, null=True)
    google_id = models.CharField(max_length=200, blank=True, null=True)
    github_id = models.CharField(max_length=200, blank=True, null=True)

    # Authentication
    password_reset_required = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    # Trackables
    login_count = models.IntegerField(default=0)
    last_login = models.DateTimeField(blank=True, null=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    login_failed_attempts = models.IntegerField(default=0)
    login_failed_attempt_ip = models.GenericIPAddressField(blank=True, null=True)

    # Permissions
    is_active = models.BooleanField(default=True, db_index=True)
    is_instructor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Model Managers
    objects = UserManager()
    active_objects = ActiveUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    # Django Admin fields
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
