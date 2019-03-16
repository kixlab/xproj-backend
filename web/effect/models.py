from django.db import models
from policy.models import Policy
from accounts.models import User
from stakeholdergroup.models import StakeholderGroup
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase, TagBase, GenericTaggedItemBase
# Create your models here.

class NewTag(TagBase):
    pass

class NewTaggedEffect(GenericTaggedItemBase):
    tag = models.ForeignKey('NewTag')
    content_object = models.ForeignKey('Effect', related_name="%(app_label)s_%(class)ss")

class TaggedEffect(TaggedItemBase):
    content_object = models.ForeignKey('Effect')

class Effect(models.Model):
    policy = models.ForeignKey('policy.Policy', related_name="effects", null=False)
    stakeholder_group = models.ForeignKey('stakeholdergroup.StakeholderGroup', related_name="effects", null=False) #TODO: Remove it!
    user = models.ForeignKey('accounts.User', related_name='effects')
    # user_policy = models.ForeignKey('userpolicy.UserPolicy', related_name='effects')
    isBenefit = models.IntegerField(default = 0)
    stakeholder_detail = models.TextField(null=True)
    description = models.TextField()
    source = models.TextField()
    tags = TaggableManager(through=TaggedEffect)
    # tags = TaggableManager(through=NewTaggedEffect, related_name="newtags")
    confidence = models.IntegerField(default = 0)
    created = models.DateTimeField(auto_now_add=True)

    is_guess = models.BooleanField(default=False)

    def __str__(self):
        return self.description
