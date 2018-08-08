from django.db import models
from accounts.models import User
from policy.models import Policy
from stakeholdergroup.models import StakeholderGroup
# Create your models here.

class UserPolicy(models.Model):
    user = models.ForeignKey('accounts.User', related_name='userpolicy', null=False)
    policy = models.ForeignKey('policy.Policy', related_name='userpolicy', null=False)
    effect_size = models.IntegerField(default = 0)
    stakeholder_group = models.ForeignKey('stakeholdergroup.StakeholderGroup', related_name='userpolicy', null=True)
    stakeholder_detail = models.TextField()
