from django.db import models
from accounts.models import User
from policy.models import Policy
from stakeholdergroup.models import StakeholderGroup
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

