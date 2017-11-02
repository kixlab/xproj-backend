from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from spatial.models import Area

class User(AbstractUser):
    year_of_birth = models.PositiveSmallIntegerField(blank=True, null=True)
    location = models.ForeignKey(Area, blank=True, null=True)

