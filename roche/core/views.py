from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Profile, Roche, Participant

class ProfileDetailView(generic.DetailView):
    model = Profile
    slug_field = 'user__username'

class RocheListView(generic.ListView):
    model = Roche

class RocheDetailView(generic.DetailView):
    model = Roche

    def get_context_data(self, **kwargs):
        context = super(RocheDetailView , self).get_context_data(**kwargs)
        participants = Participant.objects.filter(roche_id=self.kwargs['pk'])
        context['invited'] = participants.filter(status='invited')
        context['joined'] = participants.filter(status='joined')
        context['declined'] = participants.filter(status='declined')
        return context

class RocheCreate(CreateView):
    model = Roche
    fields = [
            'title',
            'description',
            'condition',
            'condition_count',
            ]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = Profile.objects.get(user_id=self.request.user.id)
        self.object.save()
        return super().form_valid(form)
