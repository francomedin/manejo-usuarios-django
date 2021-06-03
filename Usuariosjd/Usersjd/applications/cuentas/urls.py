from django.contrib import admin
from django.urls import path
from . import views
app_name = "cuenta_app"
urlpatterns = [
    path('', views.CuentaListView.as_view(), name='cuenta_list'),
    path('create/', views.CuentaCreateView.as_view(), name='cuenta_create'),
    path('detail/<pk>/', views.CuentaDetailView.as_view(), name='cuenta_detail'),
    path('update/<pk>/', views.CuentaUpdateView.as_view(), name='cuenta_update'),
    path('delete/<pk>/', views.CuentaDeleteView.as_view(), name='cuenta_delete'),

]
