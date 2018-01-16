from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from spatial.models import Area
from model_utils import Choices, FieldTracker

class User(AbstractUser):
    GENDER = Choices(
        ('female', _('female')),
        ('male', _('male')),
        ('other', _('other')),
        ('unstated', _('rather not say'))
    )

    OCCUPATION = Choices(
        ('employed', _('employed')),
        ('self-employed', _('self-employed')),
        ('unemployed', _('unemployed')),
        ('homemaker', _('homemaker')),
        ('student', _('student')),
        ('retired', _('retired')),
        ('other', _('other'))
    )

    year_of_birth = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("year of birth")  # (생년)
    )
    location = models.ForeignKey(Area,
        blank=True, null=True, verbose_name=_("area of residence")  # (거주 지역))
    )
    gender = models.CharField(
        choices=GENDER, max_length=10, verbose_name=_("gender"),  # (성별)
        default=''
    )
    occupation = models.CharField(
        choices=OCCUPATION, max_length=20, verbose_name=_("occupation"),  # (직업)
        default=''
    )

    def experiment_bucket(self, n):
        """
        Assign user to one of n buckets for experiment versions.
        This should be fixed per user per n
        """
        return self.pk % n

