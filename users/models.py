from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, name, email, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(

            name=name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    objects = MyUserManager()

    def __str__(self):
        return self.email

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


class OTP(models.Model):
    task_choice = [
        ('active', 'Active Account'),
        ('reset', 'Reset Pass'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField(editable=False, default=False),
    has_used = models.BooleanField(default=False)
    task_type = models.CharField(max_length=100, choices=task_choice, default='active')

    def __str__(self):
        return self.user
