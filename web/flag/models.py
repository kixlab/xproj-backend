from django.db import models
from effect.models import Effect
# Create your models here.

class Flag(models.Model):
    effect = models.ForeignKey('effect.Effect', related_name='flag', null=False)
    reason = models.TextField()