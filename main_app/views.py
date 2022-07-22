from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Parcel, Addon, Photo
from .forms import PickUpForm
import uuid
import boto3

#  class Mail:
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

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'mail-collector-dc'

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

def home(request):
    return render(request, 'home.html')

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

def add_photo(request, parcel_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, parcel_id=parcel_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', parcel_id=parcel_id)

def assoc_addon(request, parcel_id, addon_id):
  # Note that you can pass a toy's id instead of the whole object
  Parcel.objects.get(id=parcel_id).addons.add(addon_id)
  return redirect('detail', parcel_id=parcel_id)

class AddonsList(ListView):
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
  success_url = '/addons/'


