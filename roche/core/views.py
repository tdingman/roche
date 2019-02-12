from django.shortcuts import render
from django.views import generic
from core.models import Roche

class RocheListView(generic.ListView):
    model = Roche

class RocheDetailView(generic.DetailView):
    model = Roche
