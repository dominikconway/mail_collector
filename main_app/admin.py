from django.contrib import admin
from .models import Parcel, Photo, PickUp, Addon

admin.site.register(Parcel)
admin.site.register(PickUp)
admin.site.register(Addon)
admin.site.register(Photo)


