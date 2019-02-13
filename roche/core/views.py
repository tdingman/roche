from django.shortcuts import redirect, render
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

        profile = Profile.objects.get(user=self.request.user)
        try:
            participant = participants.get(profile=profile)
            context['show_accept_link'] = True if participant.status == 'invited' else False
        except Exception:
            context['show_join_link'] = True
        finally:
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

def join(request, pk):
    roche = Roche.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=request.user.id)

    Participant.objects.create(
            profile=profile,
            roche=roche,
            status='joined',
            )

    return redirect('roche', pk=pk)
