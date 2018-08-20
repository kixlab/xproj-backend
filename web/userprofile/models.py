from django.db import models
from accounts.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    is_participant = models.BooleanField()
    step = models.IntegerField(default=1)
    presurvey_done = models.BooleanField(default = False)