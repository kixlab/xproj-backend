from rest_framework import serializers
from policy.models import Policy
from effect.models import Effect
from policy.serializers import PolicySerializer

class EffectSerializer(serializers.ModelSerializer):
    # policy = PolicySerializer(read_only=True)
    class Meta:
        model = Effect
        fields = ('url', 'id', 'user_policy', 'policy', 'stakeholder_group', 'isBenefit', 'stakeholder_detail', 'description', 'likes')
        # read_only_fields = ('policy',)
    # def create(self, validated_data):
    #     effect = Effect()
    #     print(validated_data)
    #     return effect