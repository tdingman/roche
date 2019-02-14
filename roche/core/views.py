from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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
        context['remaining'] = participants.filter(status='remaining')
        context['eliminated'] = participants.filter(status='eliminated')

        if self.request.user.is_authenticated:
            creator = Roche.objects.get(pk=self.kwargs['pk']).created_by
            profile = Profile.objects.get(user=self.request.user)
            joined = participants.filter(status='joined')
            try:
                participant = participants.get(profile=profile)
                if participant.status == 'invited':
                    context['show_accept_link'] = True
                elif profile == creator and joined.count() > 1:
                    context['show_finalize_link'] = True
            except Exception:
                context['show_join_link'] = True
            finally:
                return context
        else:
            return context

class RocheCreate(LoginRequiredMixin, CreateView):
    model = Roche
    fields = [
            'title',
            'description',
            'condition',
            'condition_count',
            ]
    
    # This sets created_by as the logged-in user and adds them as a participant
    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        profile = Profile.objects.get(user_id=user.id)
        roche = self.object
        self.object.created_by = profile
        self.object.save()
        
        Participant.objects.create(
                profile=profile,
                roche=roche,
                status='joined',
                )

        return super().form_valid(form)

@login_required
def join(request, pk):
    roche = Roche.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=request.user.id)
    if Participant.objects.filter(profile_id=profile.id).count() == 0:
        Participant.objects.create(
                profile=profile,
                roche=roche,
                status='joined',
                )

    return redirect('roche', pk=pk)

@login_required
def accept(request, pk):
    roche = Roche.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=request.user.id)
    participant = Participant.objects.get(profile_id=profile.id)
    participant.status = 'joined'
    participant.save()
    return redirect('roche', pk=pk)

@login_required
def finalize(request, pk):
    roche = Roche.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=request.user.id)
    if roche.created_by == profile:
        participants = Participant.objects.filter(roche_id=pk)
        invited = participants.filter(status='invited')
        joined = participants.filter(status='joined')
        for i in invited:
            i.status = 'declined'
            i.save()
        for j in joined:
            j.status = 'remaining'
            j.save()
    return redirect('roche', pk=pk)
