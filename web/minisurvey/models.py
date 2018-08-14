from django.db import models
from accounts.models import User
from policy.models import Policy

# Create your models here.
class MiniSurvey(models.Model):
    user = models.ForeignKey('accounts.User', related_name='minisurvey')
    policy = models.ForeignKey('policy.Policy', related_name='minisurvey')

    first_answer = models.IntegerField()
    second_answer = models.IntegerField()
    third_answer = models.IntegerField()
    fourth_answer = models.IntegerField()