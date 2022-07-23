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
    path('parcels/<int:parcel_id>/add_pickup/', views.add_pickup, name='add_pickup'),
    path('parcels/<int:parcel_id>/add_photo/', views.add_photo, name='add_photo'),
    path('parcels/<int:parcel_id>/assoc_toy/<int:addon_id>/', views.assoc_addon, name='assoc_addon'),
    path('addons/', views.AddonsList.as_view(), name='addons_index'),
    path('addons/<int:pk>/', views.AddOnsDetail.as_view(), name='addons_detail'),
    path('addons/create/', views.AddOnsCreate.as_view(), name='addons_create'),
    path('addons/<int:pk>/update/', views.AddOnsUpdate.as_view(), name='addons_update'),
    path('addons/<int:pk>/delete/', views.AddonsDelete.as_view(), name='addons_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]