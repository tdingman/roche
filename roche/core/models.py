from django.db import models
from django.contrib.auth.models import User

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
            ('expired', 'Expired'),
            )
    status = models.CharField(
            max_length = 11,
            choices = STATUS_OPTION,
            default ='open',
            )

    performer = models.OneToOneField(
            User,
            on_delete = models.CASCADE,
            related_name = 'performer',
            )
    fulfilled_at = models.DateTimeField(
            help_text = 'When was the roche fulfilled?',
            )
    proof = models.TextField(
            help_text = 'Describe what happened',
            )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
            User,
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
    completed_at = models.DateTimeField()
    #Meta
    class Meta:
        order_with_respect_to = 'roche'
    #Methods
    def __str__(self):
        return self.id

class Participant(models.Model):

    #Fields
    user = models.ForeignKey(
            User,
            on_delete = models.CASCADE,
            )
    roche = models.ForeignKey(
            Roche,
            on_delete = models.CASCADE,
            )
    round = models.ForeignKey(
            Round,
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
            )
    #Meta
    class Meta:
        order_with_respect_to = 'round'
    #Methods
    def __str__(self):
        return self.user.username
