from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('parcels/', views.parcels_index, name='index'),
    path('parcels/<int:parcel_id>/', views.parcels_detail, name='detail'),
]