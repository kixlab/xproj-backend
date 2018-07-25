from rest_framework import serializers
from policy.models import Policy

class StakeholderGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('url', 'id', 'title', 'description')