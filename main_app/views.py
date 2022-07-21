from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Parcel
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
    return render(request, 'parcels/detail.html', {'parcel': parcel})




