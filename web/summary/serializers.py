from rest_framework import serializers
from summary.models import Summary

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ('url', 'id','stakeholder_group', 'text', 'likes')