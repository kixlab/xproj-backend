from django.db import models
from accounts.models import User
from policy.models import Policy
from stakeholdergroup.models import StakeholderGroup
from simple_history.models import HistoricalRecords
from effect.models import Effect
# Create your models here.

class UserPolicy(models.Model):
    user = models.ForeignKey('accounts.User', related_name='userpolicy', null=False)
    policy = models.ForeignKey('policy.Policy', related_name='userpolicy', null=False)
    effect_size = models.IntegerField(default = 0)
    # TODO: Add more fields to track user activity

    user_type = models.CharField(max_length = 40) # Articles / SeeStakeholders / TakePerspectives
    stakeholders_answered = models.IntegerField()
    stakeholders_seen = models.IntegerField()
    articles_seen = models.IntegerField()
    effects_seen = models.IntegerField(default=0)

    identify_done = models.BooleanField(default = False)
    guessing_done = models.BooleanField(default = False)

    initial_stance = models.IntegerField(default = 0, null = True)
    initial_opinion = models.TextField(default = '', null = True, blank = True)

    final_stance = models.IntegerField(default = 0)
    final_opinion = models.TextField(default = '', null = True, blank = True)

    fav_effects = models.ManyToManyField(Effect, related_name='favorite_userpolicy', null = True, blank = True)

    history = HistoricalRecords()


    def __str__(self):
        return "%s-%s" % (self.user.email, self.policy.title)
