from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Policy(models.Model):
    title = models.CharField(max_length=254)
    description = models.TextField()

    def __str__(self):
        return self.title
