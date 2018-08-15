from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Policy(models.Model):
    title = models.CharField(max_length=254)
    description = models.TextField()
    article1_title = models.TextField()
    article1_link = models.TextField()
    article1_text = models.TextField()
    article2_title = models.TextField()
    article2_link = models.TextField()
    article2_text = models.TextField()
    
    def __str__(self):
        return self.title
