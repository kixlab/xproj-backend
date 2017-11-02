from django.contrib.gis.db import models
from spatial.models import VotingDistrict
from django.contrib.postgres.fields import ArrayField

class Person(models.Model):
    name = models.CharField(max_length=100)
    mop_for_district = models.ForeignKey(VotingDistrict, related_name='mop', null=True)
    mayor_for_province = models.CharField(max_length=50, blank=True, null=True)
    mayor_for_district = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Promise(models.Model):
    title = models.CharField(max_length=254)
    categories = ArrayField(models.CharField(max_length=50), blank=True)
    target_groups = ArrayField(models.CharField(max_length=50), blank=True)
    person = models.ForeignKey(Person, related_name='promises',
        on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
 