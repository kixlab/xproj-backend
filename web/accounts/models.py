from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from spatial.models import Area
from model_utils import Choices, FieldTracker

class User(AbstractUser):
    GENDER = Choices(
        ('female', _('Female')),
        ('male', _('Male')),
        ('other', _('Other')),
        ('', _('Rather not say'))
    )

    OCCUPATION = Choices(
        ('employed', _('Employed')),
        ('self-employed', _('Self-employed')),
        ('unemployed', _('Unemployed')),
        ('homemaker', _('Homemaker')),
        ('student', _('Student')),
        ('retired', _('Retired')),
        ('other', _('Other'))
    )

    year_of_birth = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("Year of birth (생년)")
    )
    location = models.ForeignKey(Area,
        blank=True, null=True, verbose_name=_("Area of residence (거주 지역)")
    )
    gender = models.CharField(
        choices=GENDER, max_length=10, verbose_name=_("Gender (성별)"),
        default='', blank=True
    )
    occupation = models.CharField(
        choices=OCCUPATION, max_length=20, verbose_name=_("Occupation (직업)"),
        default=''
    )

