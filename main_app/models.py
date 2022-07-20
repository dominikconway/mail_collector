from django.db import models

class Parcel(models.Model):
    postage = models.CharField(max_length=100)
    weight = models.IntegerField()
    destination = models.CharField(max_length=100)

    def __str__(self):
        return self.postage
