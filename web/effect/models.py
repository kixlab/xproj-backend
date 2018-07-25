from django.db import models
from policy.models import Policy
from stakeholdergroup.models import StakeholderGroup
# Create your models here.

class Effect(models.Model):
    user_policy = models.ForeignKey('userpolicy.UserPolicy', related_name="effects", null=False)
    policy = models.ForeignKey('policy.Policy', related_name="effects", null=False)
    stakeholder_group = models.ForeignKey('stakeholdergroup.StakeholderGroup', related_name="effects", null=False)
    isBenefit = models.IntegerField(default = 0)
    stakeholder_detail = models.TextField()
    description = models.TextField()
    likes = models.IntegerField(default = 0)