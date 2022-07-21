from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('parcels/', views.parcels_index, name='index'),
    path('parcels/<int:parcel_id>/', views.parcels_detail, name='detail'),
    path('parcels/create/', views.ParcelCreate.as_view(), name='parcels_create'),
    path('parcels/<int:pk>/update', views.ParcelUpdate.as_view(), name='parcels_update'),
    path('parcels/<int:pk>/delete/', views.ParcelDelete.as_view(), name='parcels_delete'),
]