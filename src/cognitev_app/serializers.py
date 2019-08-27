from django.contrib.auth import get_user_model

from .models import UserProfile
from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.models import User
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.validators import UniqueValidator

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    country_code = CountryField(write_only=True)
    phone_number = PhoneNumberField(required=True,
                                    validators=[UniqueValidator(
                                        queryset=UserProfile.objects.all(),
                                        message=("A user is already registered with this phone number."))])
    gender = serializers.ChoiceField(choices=[('Male', 'Male'),
        ('Female', 'Female')])
    birth_date = serializers.DateField(required=True, write_only=True)
    avatar = serializers.ImageField()

    def get_cleaned_data_profile(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'country_code': self.validated_data.get('country_code', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'gender': self.validated_data.get('gender', ''),
            'birth_date': self.validated_data.get('birth_date', ''),
            'avatar': self.validated_data.get('avatar', ''),
        }
    def create_profile(self, user, validated_data):
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.save()
        user.UserProfile.country_code = self.validated_data.get('country_code')
        user.UserProfile.phone_number = self.validated_data.get('phone_number')
        user.UserProfile.gender = self.validated_data.get('gender')
        user.UserProfile.birth_date = self.validated_data.get('birth_date')
        user.UserProfile.avatar_date = self.validated_data.get('avatar')
        user.UserProfile.save()

    def custom_signup(self, request, user):
        self.create_profile(user, self.get_cleaned_data_profile())

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    gender = serializers.SerializerMethodField()
    avatar = serializers.ImageField()

    def get_gender(self, obj):
        return obj.get_gender_display()

    class Meta:
        model = UserProfile
        fields = ['user', 'avatar', 'phone_number', 'gender']

class UserSerializer(serializers.ModelSerializer):
    country_code = CountryField(source='UserProfile.country_code')
    birth_date = serializers.DateField(source='UserProfile.birth_date', required=True)
    avatar = serializers.ImageField(source='UserProfile.avatar')
    gender = serializers.CharField(source='UserProfile.gender')
    phone_number = PhoneNumberField(source='UserProfile.phone_number')

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password',
                  'first_name', 'last_name','avatar',
                  'last_login', 'gender', 'country_code','birth_date',
                  'phone_number']