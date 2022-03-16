from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

#from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator

#https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username/
# As we replace User class from Django to our custom User class in which we replaced the username field by email we need to adapt the UserManager as well
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        # check email is mandatory
        if not email:
            raise ValueError('The given email must be set')
        # check email is valid
        email = self.normalize_email(email)
        # create a user object
        user = self.model(email=email, **extra_fields)
        # set its hashed password
        user.set_password(password)
        # save user object to db
        user.save(using=self._db)
        return user

    # overwrite create_user to use email instead of username
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    # overwrite create_superuser to use email instead of username
    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Overwrite User class to add profile´s entries
    """

    # replacing username with email field 
    username = None
    email = models.EmailField(_('email address'), unique=True, blank=False)
    USERNAME_FIELD = 'email' # email replace username
    REQUIRED_FIELDS = [] # Removing the email field from the REQUIRED_FIELDS
    objects = UserManager()

    # "classic" fields added to our User model
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    avatar_url = models.ImageField(default='https://github.com/CMQNordic/Assets/blob/main/images/unknown-person-icon-27.jpg', upload_to='profile_pics')
    rating = models.IntegerField(default=3)
    is_instructor = models.BooleanField(default=False)
    title = models.CharField(max_length=1000, default="")
    description = models.CharField(max_length=5000, default="")
    phone = PhoneNumberField(default='+12125552368', blank=True)

    def __str__(self):
        return self.email

class Category (models.Model):
    """
    Category model (move to Category app?)
    """
    # define category choices
    KITEBOARD = 'KB'
    WING = 'WI'
    KITEFOIL = 'KF'
    SUP = 'SP'
    SURF = 'SF'
    # define  choices / value relations
    WATER_SPORT_CHOICES = [
        (KITEBOARD, 'Kiteboard'),
        (WING, 'Wingfoil'),
        (KITEFOIL, 'Kitefoil'),
        (SUP, 'SUP'),
        (SURF, 'Surf'),
    ]
    # add a category field
    category = models.CharField(
        max_length=2,
        choices=WATER_SPORT_CHOICES,
        default=KITEBOARD,
    )
    # add corresponding user field
    user = models.ForeignKey(
        'instructors.User',
        on_delete=models.CASCADE,
        blank=False,
        related_name='categories',
    )
    class Meta:
        # make the user/category a unique pair in the db 
        unique_together = ("user", "category")
    def __str__(self):
        return self.category