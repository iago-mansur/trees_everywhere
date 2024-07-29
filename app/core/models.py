"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='email address',
        help_text='Required. 255 characters or fewer. Must be a valid email address.'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='full name',
        help_text='Required. 255 characters or fewer.'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='active status',
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='staff status',
        help_text='Designates whether the user can log into this admin site.'
    )
    primary_accounts = models.ManyToManyField(
        'PrimaryAccount',
        related_name='account_users',
        blank=True,
        verbose_name='primary accounts',
        help_text='The primary accounts associated with this user.'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class PrimaryAccount(models.Model):
    """Account to aggregate users"""
    name = models.CharField(
        max_length=255,
        verbose_name='account name',
        help_text='Required. 255 characters or fewer.'
    )

    def __str__(self):
        return self.name
