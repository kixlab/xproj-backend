from django.db import models
from policy.models import Policy
from stakeholdergroup.models import StakeholderGroup

# Create your models here.

class Effect(models.Model):
    policy = models.ForeignKey('policy.Policy', related_name="effects", null=False)
    stakeholder_group = models.ForeignKey('stakeholdergroup.StakeholderGroup', related_name="effects", null=False)
    # user_policy = models.ForeignKey('userpolicy.UserPolicy', related_name='effects')
    isBenefit = models.IntegerField(default = 0)
    stakeholder_detail = models.TextField()
    description = models.TextField()
    source = models.TextField()
    empathy = models.IntegerField(default = 0)
    novelty = models.IntegerField(default = 0)

    def __str__(self):
        return self.stakeholder_detail
