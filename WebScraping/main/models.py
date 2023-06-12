from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from model_utils.managers import InheritanceManager

# first_name, last_name, phone_number, password=None kwargs ... mozna by bylo kwargsami niby


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have username")
        # if not first_name or last_name:
        #     raise ValueError("Users must have both first_name and last_name")
        # if not phone_number:
        #     raise ValueError("Users must provide phone number")
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None,  **extra_fields):
        user = self.create_user(
            email=email,
            username=username,
            password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now=True)  # auto_now_add?
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Offert(models.Model):
    objects = InheritanceManager()
    SUBJECTS = [
        ("Język polski", "Język polski"),
        ("Język angielski", "Język angielski"),
        ("Matematyka", "Matematyka"),
        ("Fizyka", "Fizyka"),
        ("Chemia", "Chemia"),
    ]

    ORIGINS = [
        ("E_KORKI", "E_KORKI"),
        ("E_KOREPETYCJE", "E_KOREPETYCJE"),
        ("KOREPETYCJE", "KOREPETYCJE"),
        ("LOCAL", "LOCAL")
    ]

    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, choices=SUBJECTS)
    locations = models.TextField(null=True)
    minPrice = models.IntegerField(null=True)
    maxPrice = models.IntegerField(null=True)
    description = models.TextField(null=True)
    link = models.URLField(max_length=255)
    from_our_user = models.BooleanField(default=False)
    origin = models.CharField(max_length=255, choices=ORIGINS, default="LOCAL")

    class Meta:
        ordering = ('-from_our_user', )

    def __str__(self):
        return f'[{self.subject}] {self.name}'


class Announcement(Offert):
    phone_number = models.CharField(max_length=50)
    author_id = models.IntegerField()
    image = models.ImageField(upload_to="images")
    phone_check = models.IntegerField(default=0)
    offer_check = models.IntegerField(default=0)

    def __str__(self):
        return f'Author: {self.name} with id {self.author_id}, subject: {self.subject}'
