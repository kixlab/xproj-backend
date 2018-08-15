from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Policy(models.Model):
    title = models.CharField(max_length=254)
    description = models.TextField(default='')
    article1_title = models.TextField(default='')
    article1_link = models.TextField(default='')
    article1_text = models.TextField(default='')
    article2_title = models.TextField(default='')
    article2_link = models.TextField(default='')
    article2_text = models.TextField(default='')

    def __str__(self):
        return self.title
