import uuid

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserProfileManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


COMPANY_SIZE_CHOICES = (
    (1, _("0 - 9")),
    (2, _("10 - 49")),
    (3, _("50 - 249")),
    (4, _("250 - 499")),
    (5, _("500 - 999")),
    (6, _("1000+"))
)

SECTOR_CHOICES = (
    (1, _("Drop 1")),
    (2, _("Drop 2"))
)

PHONE_REGEX = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class User(AbstractUser):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    company_name = models.CharField(max_length=256, blank=True, null=True,
                                    validators=[RegexValidator('[+-/%]', inverse_match=True)])
    company_size = models.IntegerField(choices=COMPANY_SIZE_CHOICES, default=1)
    sector = models.IntegerField(choices=SECTOR_CHOICES, default=1)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(validators=[PHONE_REGEX], max_length=20, blank=True, null=True)
    free_trial = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserProfileManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        return self.email

    @property
    def dashboard_name(self):
        if self.first_name and self.last_name:
            first_name = str(self.first_name)
            last_name = str(self.last_name)
            return first_name[:1] + last_name[:1]
        return "CP"
