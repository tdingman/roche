from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from core.models import Profile, Roche, Participant
from twilio.twiml.messaging_response import MessagingResponse
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose

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
            roche = Roche.objects.get(pk=self.kwargs['pk'])
            creator = roche.created_by
            profile = Profile.objects.get(user=self.request.user)
            performer = roche.performer
            joined = participants.filter(status='joined')
            try:
                participant = participants.get(profile=profile)
                if participant.status == 'invited':
                    context['show_accept'] = True
                elif profile == creator:
                    if joined.count() > 1:
                        context['show_finalize'] = True
                    elif roche.status == 'open':
                        context['show_delete'] = True
                else:
                    print('How did you get here?')
            except Exception:
                context['show_join'] = True
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
    participant = roche.participant_set.get(profile_id=profile.id)
    participant.status = 'joined'
    participant.save()
    return redirect('roche', pk=pk)

@login_required
def finalize(request, pk):
    roche = Roche.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=request.user.id)
    if roche.created_by == profile:
        roche.finalize()
    return redirect('roche', pk=pk)

@login_required
def delete(request, pk):
    roche = Roche.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=request.user.id)
    if roche.created_by == profile:
        roche.delete()
    return redirect('index')

@login_required
def fulfill(request, pk):
    roche = Roche.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=request.user.id)
    performer = roche.performer
    if profile == performer:
        roche.fulfill()
    return redirect('roche', pk=pk)

@login_required
def throw(request, pk, slug):
    if slug in dict(Participant._meta.get_field('throw').choices):
        roche = Roche.objects.get(pk=pk)
        profile = Profile.objects.get(user_id=request.user.id)
        participant = roche.participant_set.get(profile_id=profile.id)
        if participant.throw == None and participant.status == 'remaining':
            participant.throw = slug
            participant.save()
    return redirect('roche', pk=pk)

@twilio_view
def parse_sms(request):

    response = MessagingResponse()
    twilio_request = decompose(request)
    print(twilio_request.body)
    return MessagingResponse()

@twilio_view
def send_sms(request):

    print(request)
