from random import randint
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import random, string
from django.db import models
from django.contrib.auth.models import \
    (BaseUserManager, AbstractBaseUser)
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.conf import settings


# Create your models here.

REGEX_FOR_USER = '^[a-zA-z0-9]*$'


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,  password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,

        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length = 255, validators = [RegexValidator(
                                regex = REGEX_FOR_USER,
                                message = 'Username must be alphanumeric',
                                code = 'invalid_username')],
                                unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin



class ActivateProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=124)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = key_generator()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

def key_generator():
    key_generated = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(24))
    return key_generated


def send_email(instance):
    User = MyUser.objects.filter(email=instance).first()
    activation_key = User.activateprofile_set.all().first().key
    subject = "Confirm registration on MovieRaterWEB"
    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email, User.email]
    html_content = '<h3>Thank you for registering</h3><hr><br><br><p>Click ' \
                   '<a href="http://127.0.0.1:8000/accounts/register/{}">HERE</a>' \
                   ' to confirm your registration<br><br><br><strong>Best regards<br>MovieRaterWEB</strong><hr></p>' \
                    .format(activation_key)

    send_mail(subject, "", from_email, to_email, html_message=html_content, fail_silently=True)



def post_save_user(sender, instance, created, *args, **kwargs):
    if created:
        try:
            ActivateProfile.objects.create(user=instance)
            send_email(instance=instance)
        except:
            pass

post_save.connect(post_save_user, sender = settings.AUTH_USER_MODEL)