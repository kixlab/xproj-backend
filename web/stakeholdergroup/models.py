from django.db import models
from policy.models import Policy
# Create your models here.

class StakeholderGroup(models.Model):
    policy = models.ForeignKey('policy.Policy', related_name="stakeholder_group", null="False")
    name = models.CharField(max_length = 255)