from django.db import models
from accounts.models import User
from effect.models import Effect

# Create your models here.
class Novelty(models.Model):
    user = models.ForeignKey('accounts.User', related_name='novelty', null=False)
    effect = models.ForeignKey('effect.Effect', related_name='novelty', null=False)
