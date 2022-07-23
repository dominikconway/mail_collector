from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
class ParcelCreate(LoginRequiredMixin, CreateView):
    model = Parcel
    fields = ['postage', 'weight', 'destination']
    success_url = '/parcels/'

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

    

class ParcelUpdate(LoginRequiredMixin, UpdateView):
    model = Parcel
    fields = ['postage', 'weight', 'destination']

class ParcelDelete(LoginRequiredMixin, DeleteView):
    model = Parcel
    success_url = '/parcels/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def parcels_index(request):
    parcels = Parcel.objects.filter(user=request.user)
    return render(request, 'parcels/index.html', {'parcels': parcels})

@login_required
def parcels_detail(request, parcel_id):
    parcel = Parcel.objects.get(id=parcel_id)
    addons_parcel_doesnt_have = Addon.objects.exclude(id__in = parcel.addons.all().values_list('id'))
    pickup_form = PickUpForm()
    return render(request, 'parcels/detail.html', {
        'parcel': parcel, 'pickup_form': pickup_form,
        'addons' : addons_parcel_doesnt_have
        })

@login_required
def add_pickup(request, parcel_id):
    form = PickUpForm(request.POST)
    if form.is_valid():
        new_pickup = form.save(commit=False)
        new_pickup.parcel_id = parcel_id
        new_pickup.save()
    return redirect('detail', parcel_id=parcel_id)

@login_required
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

@login_required
def assoc_addon(request, parcel_id, addon_id):
  # Note that you can pass a toy's id instead of the whole object
  Parcel.objects.get(id=parcel_id).addons.add(addon_id)
  return redirect('detail', parcel_id=parcel_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class AddonsList(LoginRequiredMixin, ListView):
  model = Addon

class AddOnsDetail(LoginRequiredMixin, DetailView):
  model = Addon

class AddOnsCreate(LoginRequiredMixin, CreateView):
  model = Addon
  fields = '__all__'

class AddOnsUpdate(LoginRequiredMixin, UpdateView):
  model = Addon
  fields = ['name', 'color']

class AddonsDelete(LoginRequiredMixin, DeleteView):
  model = Addon
  success_url = '/addons/'


