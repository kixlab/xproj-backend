from django.db import models
from accounts.models import User
from effect.models import Effect

# Create your models here.
class Fishy(models.Model):
    user = models.ForeignKey('accounts.User', related_name='fishy', null=False)
    effect = models.ForeignKey('effect.Effect', related_name='fishy', null=False)
