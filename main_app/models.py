from django.db import models
from django.urls import reverse

class Parcel(models.Model):
    postage = models.CharField(max_length=100)
    weight = models.IntegerField()
    destination = models.CharField(max_length=100)

    def __str__(self):
        return self.postage

    def get_absolute_url(self):
        return reverse('detail', kwargs={'parcel_id': self.id})
