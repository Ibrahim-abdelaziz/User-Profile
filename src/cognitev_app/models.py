from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from datetime import timezone
# Create your models here.

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),)

    user = models.OneToOneField(User, related_name='UserProfile', on_delete=models.CASCADE)
    country_code = CountryField(blank_label='(Select Country)', blank=True, null=True)
    phone_number = PhoneNumberField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='img/')


    def __str__(self):
        return self.first_name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, *args, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)