from django.db import models
from stakeholdergroup.models import StakeholderGroup
# Create your models here.

class Summary(models.Model):
    stakeholder_group = models.ForeignKey('stakeholdergroup.StakeholderGroup', related_name='summary', null=False)
    text = models.TextField()
    likes = models.IntegerField()
