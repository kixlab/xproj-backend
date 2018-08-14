from rest_framework import serializers
from userpolicy.models import UserPolicy

class UserPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPolicy
        fields = ('url', 'id','user', 'policy', 'effect_size', 'stakeholders_seen', 'stakeholders_answered', 'user_type')