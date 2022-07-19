from django.shortcuts import render
from django.http import HttpResponse

class Mail:
    def __init__(self, classification, weight, destination):
        self.classification = classification
        self.weight = weight
        self.destination = destination

parcels = [
    Mail('International', 11, 'Mexico City'),
    Mail('International', 11, 'Bankok'),
    Mail('First-Class', 11, 'Dublin'),
    Mail('First-Class', 4, 'Park City'),
    Mail('Priority', 20, 'Charleston')
]



def home(request):
    return HttpResponse('<h1>Hello World</h1>')

def about(request):
    return render(request, 'about.html')

def mail_index(request):
    return render(request, 'parcels/index.html', {'parcels': parcels})

