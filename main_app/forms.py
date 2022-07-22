from django.forms import ModelForm
from .models import PickUp

class PickUpForm(ModelForm):
  class Meta:
    model = PickUp
    fields = ['date', 'type']