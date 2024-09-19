from django.urls import path
from . import views
from .views import ArticlesView

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),  # Foydalanuvchi ro'yxatdan o'tishi uchun
    path('login/', views.LoginView.as_view(), name='login'),  # Foydalanuvchi tizimga kirishi uchun
    path('me/', views.UsersMe.as_view(), name='users-me'),  # Foydalanuvchi o'z profilini ko'rishi uchun
    path('logout/', views.LogoutView.as_view(), name='logout'),  # Foydalanuvchi tizimdan chiqishi uchun
    path('password/change/', views.ChangePasswordView.as_view(), name='change-password'), # Parolni o'zgartirish uchun
    path('password/forgot/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    # Parolni unutganlar uchun so'rov yuborish
    path('password/forgot/verify/<str:otp_secret>/', views.ForgotPasswordVerifyView.as_view(), name="forgot-verify"),
    # Parolni unutganlar uchun OTP tekshiruvi
    path('password/reset/', views.ResetPasswordView.as_view(), name='reset-password'),  # Parolni tiklash
    path('articles/', ArticlesView.as_view({'get': 'list', 'post': 'create'}), name='articles-list-create'),
    # Maqolalarni ko'rish va yaratish
]