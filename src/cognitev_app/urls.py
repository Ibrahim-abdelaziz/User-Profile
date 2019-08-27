from django.urls import path, include

from cognitev_app.views import RegisterAPIView
from . import views
from django.views.generic import TemplateView
from rest_auth.views import (
                            LoginView, PasswordResetView,
                            PasswordResetConfirmView, PasswordChangeView,
                            LogoutView
                            )
from rest_auth.registration.views import RegisterView, VerifyEmailView



urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/',RegisterAPIView.as_view(), name='account_signup'),
    path('registration/', include('rest_auth.registration.urls')),
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    #path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    #path('password/reset/confirm/<str:uidb64>/<str:token>/',
            #PasswordResetConfirmView.as_view(),
            #name='rest_password_reset_confirm'),
    #path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('profile/<int:pk>/', views.ProfileAPIView.as_view()),
    path('user/<str:username>/', views.UserDetailView.as_view()),


]