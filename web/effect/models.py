from django.db import models
from policy.models import Policy
from accounts.models import User
from stakeholdergroup.models import StakeholderGroup
from taggit.managers import TaggableManager
# Create your models here.

class Effect(models.Model):
    policy = models.ForeignKey('policy.Policy', related_name="effects", null=False)
    stakeholder_group = models.ForeignKey('stakeholdergroup.StakeholderGroup', related_name="effects", null=False)
    user = models.ForeignKey('accounts.User', related_name='effects')
    # user_policy = models.ForeignKey('userpolicy.UserPolicy', related_name='effects')
    isBenefit = models.IntegerField(default = 0)
    stakeholder_detail = models.TextField()
    description = models.TextField()
    source = models.TextField()
    tags = TaggableManager()
    
    def __str__(self):
        return self.stakeholder_detail
