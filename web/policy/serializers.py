from rest_framework import serializers
from policy.models import Policy

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('url', 'id', 'title', 'description', 'article1_title', 'article1_link', 'article1_text', 'article2_title', 'article2_link', 'article2_text', 'key_stakeholders')