from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from payu.models import Transaction

# Create your models here.


highest_qualification_choices =(
    ("No formal education", "No formal education"),
    ("Primary Education", "Primary Education"),
    ("Secondary Education", "Secondary Education"),
    ("Bachelor's Degree", "Bachelor's Degree"),
    ("Master's Degree", "Master's Degree"),
)


class MyAccountManager(BaseUserManager):

    def create_user(self,first_name, last_name, email, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name, last_name, email, phone, password):
        user = self.create_user(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    first_name = models.CharField(verbose_name="First Name",max_length=30)
    last_name = models.CharField(verbose_name="Last Name",max_length=30)
    email = models.EmailField(verbose_name="Email", max_length=70, unique=True)
    phone = PhoneNumberField(help_text='Enter valid contact number with country code')
    country = CountryField(null=True, blank_label="Choose Country")
    dob = models.DateField(verbose_name="Date of Birth", max_length=8, null=True)
    hq = models.CharField(max_length=50, verbose_name="Highest Qualification", null=True, choices=highest_qualification_choices)
    pro_pic = models.ImageField(null=True, blank=True, verbose_name='Profile Picture', default='default_pic.jpg', upload_to='profile_pictures')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, verbose_name='Email Verification')
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    transactions = models.ManyToManyField(Transaction, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



