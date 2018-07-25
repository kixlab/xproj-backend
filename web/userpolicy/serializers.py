from rest_framework import serializers
from userpolicy.models import UserPolicy

class UserPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPolicy
        fields = ('url', 'id', 'effect_size', 'stance', 'is_stakeholder', 'stakeholder')