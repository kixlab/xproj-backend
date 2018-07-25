from rest_framework import serializers
from stakeholdergroup.models import StakeholderGroup

class StakeholderGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StakeholderGroup
        fields = ('url', 'id', 'policy', 'name')