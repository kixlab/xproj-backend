from django.db import models
from accounts.models import User
from effect.models import Effect

# Create your models here.
class Empathy(models.Model):
    user = models.ForeignKey('accounts.User', related_name='empathy', null=False)
    effect = models.ForeignKey('effect.Effect', related_name='empathy', null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.effect.description
