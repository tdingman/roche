from django.db import models

class Roche(models.Model):

    #Fields
    consequence = Consequence(self.id)
    condition =
    condition_count =
    status = 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_by_user')
    #Meta
    class Meta:
        ordering = 
    #Methods
    def get_absolute_url(self):
        return reverse('roche', args=[str(self.id)])
    def __str__(self):
        return self.consequence

class Round(models.Model):

    #Fields
    round_number = 1
    #Meta
    class Meta:
        ordering =
    #Methods
    def __str__(self):
        return self.round_number

class Participant(models.Model):

    #Fields
    fname = 
    lname = 
    user_id = models.ForeignKey(User)
    roche_id = models.ForeignKey(Roche)
    round_id = models.ForeignKey(Round)
    #Meta
    #Methods
    def __str__(self):
        return self.name

class Consequence(models.Model):

    #Fields
    description =
    roche_id =
    performer_id =
    fulfilled_at = 
    #Meta
    #Methods
    def __str__(self):
        return self.description
