from django.contrib import admin
from django.urls import path
from . import views
app_name = "users_app"

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='users_register'),
    path('login/', views.LoginUser.as_view(), name='users_login'),
    path('logout/', views.LogOutView.as_view(), name='users_logout'),
    path('update-password/', views.UpdatePassword.as_view(), name='users_update'),
    path('verification/<pk>/', views.CodeVerificationView.as_view(),
         name='users_verification'),
    path('update/<pk>/', views.UsersUpdateView.as_view(),
         name='users_update_profile'),
    path('profile/<pk>/', views.UserDetailView.as_view(), name='profile'),
    path('home/', views.HomeTemplateView.as_view(), name='home'),
    path('reset/', views.ResetPasswordView.as_view(), name='reset_password'),


]
