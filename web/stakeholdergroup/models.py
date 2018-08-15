from django.db import models
from policy.models import Policy
from accounts.models import User
# Create your models here.

class StakeholderGroup(models.Model):
    policy = models.ForeignKey('policy.Policy', related_name="stakeholder_group", null=False)
    name = models.CharField(max_length = 255)
    is_visible = models.BooleanField(default=True)
    author = models.ForeignKey('accounts.User', related_name="stakeholder_group_custom", null=True)

    def __str__(self):
        return self.name