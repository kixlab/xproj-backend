from django.contrib.gis.db import models
from spatial.models import VotingDistrict

class Person(models.Model):
    name = models.CharField(max_length=100)
    mop_for_district = models.ForeignKey(VotingDistrict, related_name='mop')