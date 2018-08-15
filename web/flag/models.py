from django.db import models
from effect.models import Effect
from accounts.models import User

# Create your models here.

class Flag(models.Model):
    user = models.ForeignKey('accounts.User', related_name='flag', null=False)
    effect = models.ForeignKey('effect.Effect', related_name='flag', null=False)
    reason = models.TextField()