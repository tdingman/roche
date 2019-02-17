from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    
    #Fields
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            )
    phone = models.CharField(
            max_length = 10,
            help_text = 'US cell phones only',
            )
    #Meta
    #Functions
    def __str__(self):
        return self.user.username

class Roche(models.Model):

    #Fields
    title = models.CharField(
            max_length = 300,
            help_text = 'What the person has to do',
            )
    description = models.TextField(
            help_text = 'Conditions, stipulations, etc',
            )
    CONDITION_OPTION = (
            ('win', 'Win'),
            ('loss', 'Loss'),
            )
    condition = models.CharField(
            max_length = 4,
            choices = CONDITION_OPTION,
            default = 'loss',
            )
    condition_count = models.IntegerField(
            default = 1,
            help_text = 'How many wins or losses?',
            )
    STATUS_OPTION = (
            ('open', 'Open'),
            ('in-progress', 'In Progress'),
            ('complete', 'Complete'),
            ('fulfilled', 'Fulfilled'),
            )
    status = models.CharField(
            max_length = 11,
            choices = STATUS_OPTION,
            default ='open',
            )
    performer = models.ForeignKey(
            Profile,
            blank=True,
            null = True,
            on_delete = models.CASCADE,
            related_name = 'performer',
            )
    fulfilled_at = models.DateField(
            help_text = 'When was the roche fulfilled?',
            blank = True,
            null = True,
            )
    proof = models.TextField(
            help_text = 'Describe what happened',
            blank = True,
            )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
            Profile,
            on_delete = models.CASCADE,
            related_name = 'created_by',
            )
    #Meta
    class Meta:
        ordering = ['-created_at']
    #Methods
    def get_absolute_url(self):
        return reverse('roche', args=[str(self.id)])
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def finalize(self):
        round = Round.objects.create(
                roche = self,
                number = 1,
                )

        invited = self.participant_set.filter(status='invited')
        invited.update(status = 'declined')
        joined = self.participant_set.filter(status='joined')
        joined.update(status = 'remaining')
        
        remaining = self.participant_set.filter(status='remaining')
        remaining.update(round = round)

        self.status ='in-progress'
        self.save()
    def fulfill(self):
        self.fulfilled_at = timezone.now()
        self.proof = 'hi'
        self.save()
    def get_latest_round(self):
        return self.round_set.latest('created_at')

class Round(models.Model):

    #Fields
    roche = models.ForeignKey(
            Roche,
            on_delete = models.CASCADE,
            )
    number = models.IntegerField(
            default = 1,
            )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
            blank=True,
            null=True,
            )
    #Meta
    class Meta:
        order_with_respect_to = 'roche'
    #Methods
    def __str__(self):
        return self.roche.title + ' - ' + str(self.number)
    
    def eliminate(self, participants):
        participants.update(status='eliminated')

    def evaluate(self):
        participants = self.participant_set.filter(status='remaining')
        participant_count = participants.count()

        if participants.filter(throw=None).count() == 0:
            rock = participants.filter(throw='rock')
            paper = participants.filter(throw='paper')
            scissors = participants.filter(throw='scissors')

            rock_count = rock.count()
            paper_count= paper.count()
            scissors_count = scissors.count()

            condition = self.roche.condition

            if rock_count > 0 and paper_count > 0 and scissors_count > 0:
                pass
            elif rock_count == participant_count or paper_count == participant_count or scissors_count == participant_count:
                pass
            elif rock_count == 0:
                self.eliminate(scissors) if condition == 'loss' else self.eliminate(paper)
            elif paper_count == 0:
                self.eliminate(rock) if condition == 'loss' else self.eliminate(scissors)
            elif scissors_count == 0:
                self.eliminate(paper) if condition == 'loss' else self.eliminate(rock)
            else:
                print('how did you get here?')
            
            remaining = self.participant_set.filter(status='remaining')
            if remaining.count() > 1:
                newround = Round.objects.create(
                    roche=self.roche,
                    number = self.number + 1,
                    )

                remaining.update(throw=None)
                remaining.update(round=newround)
            else:
                roche = self.roche
                roche.status = 'complete'
                roche.performer = remaining[0].profile
                roche.save()

            self.completed_at = timezone.now()
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Participant(models.Model):

    #Fields
    profile = models.ForeignKey(
            Profile,
            on_delete = models.CASCADE,
            )
    roche = models.ForeignKey(
            Roche,
            on_delete = models.CASCADE,
            )
    round = models.ForeignKey(
            Round,
            blank=True,
            null=True,
            on_delete = models.CASCADE,
            )
    PARTICIPANT_STATUS = (
            ('invited', 'Invited'),
            ('joined', 'Joined'),
            ('declined', 'Declined'),
            ('remaining', 'Remaining'),
            ('eliminated', 'Eliminated')
            )
    status = models.CharField(
            max_length = 10,
            choices = PARTICIPANT_STATUS,
            default = 'invited'
            )
    THROW_OPTION = (
            ('rock', 'Rock'),
            ('paper', 'Paper'),
            ('scissors', 'Scissors')
            )
    throw = models.CharField(
            max_length = 8,
            choices = THROW_OPTION,
            blank = True,
            null = True,
            )
    #Meta
    class Meta:
        order_with_respect_to = 'round'
    #Methods
    def __str__(self):
        return self.roche.title + ' - ' + self.profile.user.username
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.round:
            self.round.evaluate()
