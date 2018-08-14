from django.db import models
from accounts.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    is_participant = models.BooleanField()
