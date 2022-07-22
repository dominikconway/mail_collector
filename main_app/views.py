from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Parcel, Addon
from .forms import PickUpForm
from django.http import HttpResponse

# class Mail:
#     def __init__(self, postage, weight, destination):
#         self.postage = postage
#         self.weight = weight
#         self.destination = destination

# parcels = [
#     Mail('International', 11, 'Mexico City'),
#     Mail('International', 11, 'Bankok'),
#     Mail('First-Class', 11, 'Dublin'),
#     Mail('First-Class', 4, 'Park City'),
#     Mail('Priority', 20, 'Charleston')
# ]

#Class Based Views
class ParcelCreate(CreateView):
    model = Parcel
    fields = '__all__'
    success_url = '/parcels/'

class ParcelUpdate(UpdateView):
    model = Parcel
    fields = ['postage', 'weight', 'destination']

class ParcelDelete(DeleteView):
    model = Parcel
    success_url = '/parcels/'

####################
def home(request):
    return HttpResponse('<h1>Hello World</h1>')

def about(request):
    return render(request, 'about.html')

def parcels_index(request):
    parcels = Parcel.objects.all()
    return render(request, 'parcels/index.html', {'parcels': parcels})

def parcels_detail(request, parcel_id):
    parcel = Parcel.objects.get(id=parcel_id)
    addons_parcel_doesnt_have = Addon.objects.exclude(id__in = parcel.addons.all().values_list('id'))
    pickup_form = PickUpForm()
    return render(request, 'parcels/detail.html', {
        'parcel': parcel, 'pickup_form': pickup_form,
        'addons' : addons_parcel_doesnt_have
        })

def add_pickup(request, parcel_id):
    form = PickUpForm(request.POST)
    if form.is_valid():
        new_pickup = form.save(commit=False)
        new_pickup.parcel_id = parcel_id
        new_pickup.save()
    return redirect('detail', parcel_id=parcel_id)

class AddonList(ListView):
  model = Addon

class AddOnsDetail(DetailView):
  model = Addon

class AddOnsCreate(CreateView):
  model = Addon
  fields = '__all__'

class AddOnsUpdate(UpdateView):
  model = Addon
  fields = ['name', 'color']

class AddonsDelete(DeleteView):
  model = Addon
  success_url = '/addon/'

def assoc_addon(request, parcel_id, addon_id):
  # Note that you can pass a toy's id instead of the whole object
  Parcel.objects.get(id=parcel_id).addons.add(addon_id)
  return redirect('detail', parcel_id=parcel_id)
