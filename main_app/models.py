from datetime import date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

TYPES = (
    ('L', 'Letter'),
    ('P', 'Package'),
    ('F', 'Flat')
)

class Addon(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('addons_detail', kwargs={'pk': self.id})

class Parcel(models.Model):
    postage = models.CharField(max_length=100)
    weight = models.IntegerField()
    destination = models.CharField(max_length=100)
    addons = models.ManyToManyField(Addon)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.postage

    def get_absolute_url(self):
        return reverse('detail', kwargs={'parcel_id': self.id})


class PickUp(models.Model):
    date = models.DateField('Pick up Date')
    type = models.CharField(max_length=1,
    choices=TYPES,
    default=TYPES[0][0]
    )

    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_type_display()} on {self.date}"    

    class Meta:
        ordering = ['-date']
    
class Photo(models.Model):
  url = models.CharField(max_length=200)
  parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for cat_id: {self.parcel_id} @{self.url}"